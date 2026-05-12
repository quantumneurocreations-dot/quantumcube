#!/bin/bash
# QI Auto Morning Briefing
# Runs daily at 7am via cron. Speaks via Owen (ElevenLabs).
# Cron entry: 0 7 * * * /Users/qnc/Projects/quantumcube/scripts/qi-morning-auto.sh

source ~/.zshrc
cd /Users/qnc/Projects/quantumcube
python3 scripts/morning-briefing.py --speak >> /tmp/qi-briefing.log 2>&1
