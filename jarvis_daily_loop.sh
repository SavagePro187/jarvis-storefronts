#!/usr/bin/env bash
set -e

WORKSPACE="$HOME/Projects/active/jarvishive"
LOG_OUT="$WORKSPACE/orchestrator_stdout.log"

echo "========================================================" >> "$LOG_OUT"
echo "[*] Launching Multi-Model Performance Run: $(date)" >> "$LOG_OUT"
echo "========================================================" >> "$LOG_OUT"

cd "$WORKSPACE"

# Benchmark Intent Parsing (qwen2.5:1.5b)
echo "[+] Profiling Intent Classifier..."
START_TIME=$(date +%s.%N)
./parse_incoming_intents.py "I am looking for automated sales scaling engines." >> "$LOG_OUT"
END_TIME=$(date +%s.%N)
INTENT_DIFF=$(echo "$END_TIME - $START_TIME" | bc)
echo "    ➔ Intent Processing Latency: ${INTENT_DIFF} seconds"

# Benchmark Orchestration Writing Loops (qwen2.5:3b / llama3)
echo "[+] Profiling Master Copy Engine..."
sqlite3 jarvis_accounting.db "DELETE FROM outbound_pitch_staging;"
START_TIME=$(date +%s.%N)
./jarvis_master_orchestrator.py >> "$LOG_OUT"
END_TIME=$(date +%s.%N)
ORCH_DIFF=$(echo "$END_TIME - $START_TIME" | bc)
echo "    ➔ Master Generation Loop Latency: ${ORCH_DIFF} seconds"

# Benchmark Storefront Compiler CSS (qwen2.5-coder:1.5b)
echo "[+] Profiling UI Compilation Layer..."
START_TIME=$(date +%s.%N)
./tool_storefront_builder.py >> "$LOG_OUT"
END_TIME=$(date +%s.%N)
CODE_DIFF=$(echo "$END_TIME - $START_TIME" | bc)
echo "    ➔ UI Compiler Generation Latency: ${CODE_DIFF} seconds"

echo "========================================================"
echo "⚡ J.A.R.V.I.S. MULTI-MODEL PERFORMANCE BENCHMARK RESULTS ⚡"
echo "========================================================"
echo "🔹 Intent Parsing Model (qwen2.5:1.5b)  : ${INTENT_DIFF}s"
echo "🔹 Copy Generator Model (qwen2.5:3b)    : ${ORCH_DIFF}s"
echo "🔹 Layout Visual Model (qwen-coder:1.5b): ${CODE_DIFF}s"
echo "========================================================"
