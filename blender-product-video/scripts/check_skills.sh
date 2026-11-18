#!/bin/bash
# usage: check_skills.sh   checks the Blender skills this workflow pilots (github.com/arjun988/blender-skills, MIT)
# Looks in ~/.claude/skills and ./.claude/skills. Exit 0 = all there, 1 = prints what is missing and how to install it.
NEED="blender-director hard-surface prop-artist materials texture-workflow lookdev lighting camera-cinematography animation geometry-nodes procedural-modeling rendering"
MISS=""
for s in $NEED; do [ -f ~/.claude/skills/$s/SKILL.md ] || [ -f .claude/skills/$s/SKILL.md ] || MISS="$MISS $s"; done
[ -z "$MISS" ] && { echo "SKILLS_OK"; exit 0; }
echo "MISSING:$MISS"
echo "install (after the user's ok):"
echo "  git clone --depth 1 https://github.com/arjun988/blender-skills.git /tmp/blender-skills"
echo "  for s in$MISS; do cp -R /tmp/blender-skills/.claude/skills/\$s ~/.claude/skills/; done"
exit 1
