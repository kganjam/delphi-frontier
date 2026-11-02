#!/usr/bin/env bash
# Wait for the frame renderer to exit, then assemble a watchable-length video.
# 3374 frames at 20 fps would be 169 s for 10 s of simulated time; subsample 6x
# and run at 25 fps for about 22 s.
set -u
D=/data/scratch/designspaces/xenobot
bash /data/worktrees/delphi-frontier/design-spaces/../../../home/ubuntu/git/morphoswarm/scripts/wait_until_gone.sh 2>/dev/null || true
while pgrep -f "[r]ender_swarm.py" > /dev/null; do sleep 5; done
N=$(ls "$D/data/anim_frames" | wc -l)
echo "frames: $N"
ffmpeg -y -loglevel error -framerate 25 -i "$D/data/anim_frames/f%05d.png" \
  -vf "select='not(mod(n\,6))',setpts=N/25/TB,scale=900:-2,pad=ceil(iw/2)*2:ceil(ih/2)*2" \
  -c:v libx264 -pix_fmt yuv420p -crf 23 -r 25 -threads 2 "$D/figures/cargo-swarm.mp4"
echo "FFMPEG-EXIT=$?"
ls -la "$D/figures/cargo-swarm.mp4"
ffprobe -v error -show_entries format=duration,size -show_entries stream=width,height,nb_frames \
  -of default=noprint_wrappers=1 "$D/figures/cargo-swarm.mp4"
