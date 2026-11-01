set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq >/dev/null && apt-get install -y -qq python3-pip >/dev/null
pip install -q "openmm[cuda12]==8.6.1" pdbfixer numpy 2>&1 | tail -2
nvidia-smi --query-gpu=name,driver_version --format=csv
python3 /in/md_job.py "$MD_SEED" "$MD_NS" "$MD_TAG"
