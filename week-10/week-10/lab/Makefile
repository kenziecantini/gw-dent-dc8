###############################################################################
# Cyber-Lab Makefile – cross-platform & sudo-aware
###############################################################################

# ---------------------------------------------------------------------------
# 0. Project settings
# ---------------------------------------------------------------------------
PROJECT        ?= week10
BASE_DIR       := compose
STEP1_YML      := $(BASE_DIR)/docker-compose.step-1.yml
STEP2_YML      := $(BASE_DIR)/docker-compose.step-2.yml
STEP3_YML      := $(BASE_DIR)/docker-compose.step-3.yml

REPORT_DIR     := reports
ABS_REPORT_DIR := $(abspath $(REPORT_DIR))
BEFORE_REPORT  := $(REPORT_DIR)/zap-before.html
AFTER_REPORT   := $(REPORT_DIR)/zap-after.html
ZAP_IMAGE      := zaproxy/zap-stable

PUBLIC_NET     := $(PROJECT)_public

# ---------------------------------------------------------------------------
# 1. Do we need sudo?
# ---------------------------------------------------------------------------
DOCKER_OK := $(shell docker info >/dev/null 2>&1 && echo yes)
ifeq ($(DOCKER_OK),yes)
  SUDO :=
else
  SUDO := sudo
endif

# ---------------------------------------------------------------------------
# 2. Choose “docker compose” vs. “docker-compose”
# ---------------------------------------------------------------------------
ifeq ($(shell uname -s),Darwin)
  DOCKER_COMPOSE := $(SUDO) docker compose
else
  ifneq (, $(shell command -v docker-compose))
    DOCKER_COMPOSE := $(SUDO) docker-compose
  else
    DOCKER_COMPOSE := $(SUDO) docker compose
  endif
endif
COMPOSE := $(DOCKER_COMPOSE) -p $(PROJECT)

# ---------------------------------------------------------------------------
# 3. Targets
# ---------------------------------------------------------------------------
.PHONY: step-1 step-2 step-3 step-4 step-5 step-6 step-7 help sync

###############################################################################
# 1️⃣  Baseline: Juice-Shop + ZAP
###############################################################################
step-1: ## spin-up vulnerable stack & run baseline scan
	@echo ">>> [1] Bootstrapping vulnerable stack..."
	$(COMPOSE) -f $(STEP1_YML) up -d

	@echo ">>> Preparing reports directory..."
	@mkdir -p $(REPORT_DIR)
	$(SUDO) chmod 777 $(REPORT_DIR)

	@echo ">>> Running baseline ZAP scan..."
	$(SUDO) docker run --rm --network $(PUBLIC_NET) \
		-v $(ABS_REPORT_DIR):/zap/wrk \
		-t $(ZAP_IMAGE) \
		zap-baseline.py -t http://juice:3000 -r $(notdir $(BEFORE_REPORT)) || true
	@echo "Baseline report: $(BEFORE_REPORT)"

###############################################################################
# 2️⃣  Add WAF + Suricata
###############################################################################
step-2: ## bring up WAF & IDS
	@echo ">>> [2] Adding WAF + Suricata..."
	$(COMPOSE) -f $(STEP1_YML) -f $(STEP2_YML) up -d # --force-recreate

	@echo "Browse → http://localhost  (through the WAF)"
	@echo "Tail  → $(DOCKER_COMPOSE) -p $(PROJECT) logs -f suricata"

###############################################################################
# 3️⃣  Re-scan through the WAF & diff
###############################################################################
step-3: ## run second scan & diff results
	@echo ">>> [3] Re-scanning via WAF..."
	$(SUDO) docker run --rm --network $(PUBLIC_NET) \
		-v $(ABS_REPORT_DIR):/zap/wrk \
		-t $(ZAP_IMAGE) \
		zap-baseline.py -t http://waf:8080 -r $(notdir $(AFTER_REPORT)) || true
	@echo "New report: $(AFTER_REPORT)"
	@echo "----- DIFF (before vs after) -----"
	-@diff -u $(BEFORE_REPORT) $(AFTER_REPORT) || true
	@echo "----------------------------------"

###############################################################################
# 4️⃣  Analyze scan reports
###############################################################################
step-4: ## analyze before and after scan reports
	@echo ">>> [4] Analyzing scan reports..."
	python3 analyze_reports.py $(BEFORE_REPORT) $(AFTER_REPORT)

###############################################################################
# 5️⃣  Cheat-sheet talking points
###############################################################################
step-5: ## print ZTA / DiD / ASA bullets
	@echo "Zero-Trust        : WAF = Policy Enforcement Point (PEP)"
	@echo "Defence-in-Depth  : WAF (L7) → Suricata (L3/4) → App"
	@echo "ASA-style edge    : WAF stands in for a perimeter firewall"

###############################################################################
# 6️⃣  15-minute live demo script
###############################################################################
step-6: ## reminder script for presenters
	@echo "1) make step-1  – baseline"
	@echo "2) attack http://localhost:3000"
	@echo "3) make step-2  – add defences"
	@echo "4) attack http://localhost (see 403 + IDS logs)"
	@echo "5) make step-3  – re-scan & diff"
	@echo "6) make step-4  – analyze reports"
	@echo "7) discuss step-5 mapping"

###############################################################################
# 7️⃣  Destroy environment
###############################################################################
step-7: ## stop containers & clean host
	@echo ">>> Destroying environment..."
	$(COMPOSE) down -v --remove-orphans
	$(SUDO) docker volume prune -f
	$(SUDO) docker network prune -f
	@echo "Environment clean."

###############################################################################
# Help
###############################################################################
help: ## show help
	@printf "\nTargets:\n\n"
	@grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*##"}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
	@printf "\n"

###############################################################################
# Optional: push local dir to remote host
###############################################################################
sync: ## rsync to VM (edit host/key as needed)
	rsync -avuz -e 'ssh -i ~/.ssh/keys/seas-8405.pem' . ubuntu@100.28.58.31:lab/

clean: step-7        ## alias – same as step-7