# Trabalho em equipe (2 a 3 pessoas) — CI + Promoção (Delivery) com Jenkins, Sonar e Trivy (Docker/Compose)

## Objetivo

Construir um ambiente com **Jenkins ou similar + SonarQube**:

1. **Pipeline principal (CI)**: build + testes + Sonar + Trivy scan repo + Docker build + Trivy image + criação de tag Git (somente `main`).
A aplicação será uma **aplicação web**, com **pelo menos duas funcionalidades que acessam banco de dados** (ex.: cadastrar e consultar).

---

# Entrega

* **Repositório Git externo** (ex.: GitHub) contendo todos os arquivos necessários.

# Requisitos do repositório

## Estrutura mínima

* Aplicação (qualquer linguagem suportada por Docker)
* Banco de dados (via Docker Compose na stack de deploy)
* `Dockerfile` da aplicação
* `tests/` e suíte de testes executável em CI
* `sonar-project.properties` (ou equivalente)
* `deploy/compose.yaml` (stack deploy: app + DB, separada)
* `README.md` reprodutível

## Requisito funcional da aplicação

* Deve ser **web**
* Deve possuir **pelo menos duas funcionalidades** que **acessam banco de dados**, por exemplo:

  * cadastro (CREATE)
  * consulta (READ)
  * (pode ser update/delete também, mas pelo menos duas)

---

# Pipeline 1 — Principal (CI)

## Stages obrigatórios

1. Checkout (repo externo)
2. Build (preparação/compilação conforme linguagem)
3. Unit tests
4. SonarQube scan (incluindo cobertura)
5. Trivy repo scan (filesystem scan do repositório)
6. Docker build (imagem)
7. Trivy image scan (imagem criada)
8. Create Git tag (somente em `main`, e não PR)

## Regras obrigatórias de qualidade e segurança

* **Cobertura mínima: 50%** (medida no Sonar e visível no vídeo), se for menos que 50% o pipeline quebra.
* **Trivy: não pode haver HIGH ou CRITICAL**

  * o pipeline deve falhar se encontrar HIGH/CRITICAL

## Tag Git

* Deve ser criada somente:

  * após merge no `main`
  * quando o build não for PR
  * quando pipeline estiver verde
* A tag deve ser **publicada no repositório remoto** (GitHub)

---

# Deploy (manual) via Docker Compose

## Regras

* O deploy será feito **manualmente**, fora do Jenkins, usando:

  * `deploy/compose.yaml`
* Deve ser possível reiniciar a stack quando necessário:

  * `docker compose down && docker compose up -d` (ou equivalente)
* O compose deve usar **tag** gerada/promovida para definir a imagem

---

# Restrições

* Não compartilhar aplicação entre equipes (deve ser única)
* Sonar deve ser exibido com dashboard atualizado
* Tag deve existir no Git remoto (GitHub)

# Trabalho em equipe (3 pessoas) — CI + Promoção (Delivery) com Jenkins, Sonar e Trivy (Docker/Compose)

## Objetivo

Construir um ambiente com **Jenkins (ou similar) + SonarQube** e implementar o pipelines:

1. **Pipeline de promoção (Delivery)**: promoção de tags por ambiente (DEV → STG → PROD) usando `docker tag`, sem deploy automático (deploy é manual via compose).

A aplicação será uma **aplicação web**, com **pelo menos duas funcionalidades que acessam banco de dados** (ex.: cadastrar e consultar).

---

# Entrega

## Entregável único

* **Repositório Git externo** (ex.: GitHub) contendo todos os arquivos necessários.
* **Link para o video** com a equipe e camera visivel. Participação da equipe na explicação.

## Evidência obrigatória no video

* **Vídeo de 15 minutos** mostrando execução real, com a equipe completa, incluindo:

  1. Subir a stack de CI (Jenkins + Sonar + DB do Sonar, se necessário) via Docker Compose
  2. **Configurar o Sonar** para o projeto (token + projeto + execução de análise)
  3. Executar o pipeline principal e:
     . mostrar que a análise no Sonar gerou **métricas visíveis** (ex.: coverage, bugs, vulnerabilities, code smells, quality gate/status)
  4. Mostrar a **tag Git publicada no repositório remoto**, seguindo versionamento semantico (ex.: GitHub tags/releases list)
  5. Mostrar a **tag no docker localmente**
  6. Realizar **deploy manual** via `deploy/compose.yaml`, reiniciando a stack quando necessário
  7. Executar o pipeline de promoção (com parâmetros) e mostrar:
     . promoção DEV e deploy manual
     . promoção STG e deploy manual
     . promoção PROD e deploy manual
  8. Demonstrar a aplicação web funcionando e evidenciar as 2 funcionalidades
  9. Demostrar historico de build de pelo menos 5 execuções e alterações
  10. Testar validação de deploy em prod sem a tag em STG. O pipeline de promotion deve falhar.

> Observação: deploy é **manual** (fora do pipeline). O pipeline só gera tags e promove tags.

---

# Deploy (manual) via Docker Compose

## Regras

* O deploy será feito **manualmente**, fora do Jenkins, usando:
  * `deploy/compose.yaml`
* Deve ser possível reiniciar a stack quando necessário:
  * `docker compose down && docker compose up -d` (ou equivalente)
* O compose deve usar **tag** gerada/promovida para definir a imagem

## Testes pós-deploy (obrigatórios no vídeo)

* Deve haver uma forma simples de testar a aplicação:
  * endpoints web
  * e evidência que a versão/tag atual está rodando (ex.: `/version`)

---

# Pipeline 2 — Promoção por ambiente (Delivery)

## Parâmetros obrigatórios

* `TAG` (string) — ex.: `v1.2.3`
* `ENVIRONMENT` (choice): `DEV`, `STG`, `PROD`

## Resultado da promoção (tags padrão)

* `DEV`: `dev-<TAG>` (ex.: `dev-v1.2.3`)
* `STG`: `stg-<TAG>` (ex.: `stg-v1.2.3`)
* `PROD`: `prod-<TAG>` (ex.: `prod-v1.2.3`)

## Cadeia obrigatória

* Só promove para STG se existir DEV daquela versão
* Só promove para PROD se existir STG daquela versão

## O pipeline de promoção deve fazer

1. Validar parâmetros
2. Validar cadeia DEV → STG → PROD
3. `docker tag` para gerar tag do ambiente
4. Evidência no log de qual imagem/tag foi promovida

> Importante: o pipeline de promoção **não faz deploy**. O deploy é manual via compose e deve ser mostrado no vídeo.
