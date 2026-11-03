# Drives the UNMODIFIED coRal R code (jrcunning/coRal, MIT, commit 7c90f9b) so the
# Python port can be checked against it. Sources only the four numeric files.
args <- commandArgs(trailingOnly=TRUE)
src <- args[1]; outdir <- args[2]
for (f in c("synth.R","def_pars.R","init_env.R","run_coral.R")) source(file.path(src,f))

time <- seq(0, 365, 0.1)
pars <- def_pars()
keep <- c("time","H","S","jCP","jeL","jNPQ","cROS","jST","jSG","jHG","jCO2","jL","rhoN","jeC")

# Three scenarios: healthy constant, light-limited constant, seasonal light.
scen <- list(
  healthy  = list(L=c(30,30,0),  N=c(1e-6,1e-6,0), X=c(0,0,0)),
  lowlight = list(L=c(10,10,0),  N=c(1e-6,1e-6,0), X=c(0,0,0)),
  seasonal = list(L=c(15,40,2),  N=c(1e-6,1e-6,0), X=c(0,0,0)),
  fed      = list(L=c(30,30,0),  N=c(1e-6,1e-6,0), X=c(1e-6,1e-6,0))
)
for (nm in names(scen)) {
  e <- scen[[nm]]
  env <- init_env(time=time, L=e$L, N=e$N, X=e$X)
  r <- run_coral(time=time, env=env, pars=pars)
  k <- keep[keep %in% names(r)]
  write.csv(cbind(r[, k], L=env$L), file.path(outdir, paste0("coRal_", nm, ".csv")), row.names=FALSE)
  n <- nrow(r)
  cat(sprintf("%-9s H=%.6g S=%.6g S/H=%.6f cROS=%.6f\n", nm, r$H[n], r$S[n], r$S[n]/r$H[n], r$cROS[n]))
}
