#!/bin/bash
# Script to reproduct results

DIMS="10"
MODEL="poincare"

while true; do
  case "$1" in
    -d | --dim ) DIMS=$2; shift; shift ;;
    -m | --model ) MODEL=$2; shift; shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

USAGE="usage: ./train-nouns.sh -d <dim> -m <model>
  -d: dimensions to use
  -m: model to use (poincare)
  Example: ./train-nouns.sh -m poincare -d 10
"

case "$MODEL" in
  "poincare" ) EXTRA_ARGS=("-lr" "1.0");;
  * ) echo "$USAGE"; exit 1;;
esac

# todo: -sparse
python3 embed.py \
  -checkpoint checkpoints/nouns-10d.tf \
  -dset wordnet/noun_closure.csv \
  -epochs 1500 \
  -negs 50 \
  -burnin 20 \
  -dampening 0.75 \
  -eval_each 1 \
  -fresh \
  -sparse \
  -burnin_multiplier 0.01 \
  -neg_multiplier 0.1 \
  -dampening 1.0 \
  -batchsize 50 \
  -manifold "$MODEL" \
  -dim "$DIMS" \
  "${EXTRA_ARGS[@]}"
