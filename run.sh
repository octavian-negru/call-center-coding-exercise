# shellcheck disable=SC2046
docker run --rm -v $(pwd)/call_center:/call_center/ -it call-center:latest | tee call_center/stats/last_run_stats.log
