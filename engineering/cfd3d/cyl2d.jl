# 2-D cylinder fidelity control, implementing cyl2d_contract.json (frozen before any run).
# Usage: julia --project=engineering/cfd3d/env engineering/cfd3d/cyl2d.jl OUT.json RUN_ID [TIMING nsteps]
#   RUN_ID in R1, R2, R3_domain, M1_mutant (parameters read from the contract, not from this file).
#   TIMING: step the run's exact domain nsteps times and record wall time and dt only. It never calls a
#   force or pressure routine, so a timing run cannot reveal the control's result before its band is frozen.
using WaterLily, StaticArrays, JSON
const GPU = get(ENV, "CFD3D_GPU", "0") == "1"
GPU && @eval using CUDA
memtype() = GPU ? CUDA.CuArray : Array
const CONTRACT = JSON.parsefile(joinpath(@__DIR__, "cyl2d_contract.json"))

function build(run)
    nD, H, Re = run["n_D"], run["H"], run["Re"]
    D = Float32(nD); R = D / 2; U = 1f0
    @assert H == 60 || H == 120
    c = SA[(H / 2f0) * D, (H / 2f0) * D]               # square H, centred cylinder (30 D each side for H = 60)
    body = AutoBody((x, t) -> √sum(abs2, x .- c) - R)
    bump = c + SA[2D, 0f0]
    u0(i, x) = i == 1 ? U : 0.01f0 * U * exp(-sum(abs2, x .- bump) / D^2)
    sim = Simulation((H * nD, H * nD), (U, 0f0), D; ν=U * D / Re, body, u0, T=Float32, exitBC=true, mem=memtype())
    sim, D, R, U, c
end

function timing(run, nsteps)
    sim, D, _, _, _ = build(run)
    sim_step!(sim); sim_step!(sim)                     # compile outside the timed loop
    dts = Float64[]
    wall = @elapsed for _ in 1:nsteps
        sim_step!(sim); push!(dts, sim.flow.Δt[end])
    end
    cells = prod(size(sim.flow.p))
    Dict("mode" => "TIMING", "cells" => cells, "steps" => nsteps, "wall_s" => wall,
         "ns_per_cell_step" => 1e9wall / (nsteps * cells), "dt_grid_mean" => sum(dts) / length(dts),
         "dt_grid_last" => dts[end], "steps_per_D_over_U_at_this_dt" => D / dts[end],
         "note" => "start-up dt; the developed wake has a higher peak speed, so later dt is smaller (estimate only)")
end

"Wall points and the three off-wall sample points per angle, in grid coordinates."
function stations(R, c, n=720)
    θ = range(0, 2π; length=n + 1)[1:end-1]
    nrm = [SA[Float32(cos(t)), Float32(sin(t))] for t in θ]
    pts = [[c + (R + k) * nn for nn in nrm] for k in (1.5f0, 2.5f0, 3.5f0)]
    nrm, pts
end

function run_case(run)
    sim, D, R, U, c = build(run)
    t_end, t0 = CONTRACT["time"]["t_end"], CONTRACT["time"]["transient_discarded_before"]
    nrm, pts = stations(R, c)
    mem = memtype()
    dpts = [mem(p) for p in pts]
    ny = size(sim.flow.p, 2)
    ts, cd, cdp, cl = Float64[], Float64[], Float64[], Float64[]
    cp_sum = zeros(Float64, length(nrm)); cp_t = Float64[]; nsteps = 0
    wall = @elapsed while sim_time(sim) < t_end
        sim_step!(sim); nsteps += 1
        ft = WaterLily.total_force(sim); fp = WaterLily.pressure_force(sim)
        push!(ts, sim_time(sim)); push!(cd, -2ft[1] / (U^2 * D)); push!(cl, -2ft[2] / (U^2 * D))
        push!(cdp, -2fp[1] / (U^2 * D))
        isfinite(cd[end]) || break
        if ts[end] >= t0 && nsteps % 10 == 0
            p = sim.flow.p
            pref = sum(Array(@view p[2, 2:ny-1])) / (ny - 2)
            s = [Array(WaterLily.interp.(dp, Ref(p))) for dp in dpts]    # samples at R + 1.5, 2.5, 3.5 h
            # quadratic through (1.5, s1), (2.5, s2), (3.5, s3), evaluated at 0 (the wall)
            pw = @. (35 * s[1] - 42 * s[2] + 15 * s[3]) / 8
            cp_sum .+= (pw .- pref) ./ (0.5U^2); push!(cp_t, ts[end])
        end
    end
    Dict("mode" => "RUN", "n_D" => run["n_D"], "H" => run["H"], "Re" => run["Re"], "grid" => collect(size(sim.flow.p)),
         "steps" => nsteps, "t_end_reached" => ts[end], "finite" => all(isfinite, cd), "wall_s" => wall,
         "ns_per_cell_step" => 1e9wall / (nsteps * prod(size(sim.flow.p))),
         "t" => ts, "Cd" => cd, "Cd_p" => cdp, "Cl" => cl,
         "surface" => Dict("angles" => length(nrm), "samples" => length(cp_t),
                           "Cp_wall_mean" => cp_sum ./ max(length(cp_t), 1), "t_first" => isempty(cp_t) ? nothing : cp_t[1]))
end

function main(out, id, mode="RUN", nsteps="200")
    run = CONTRACT["runs"][id]
    r = mode == "TIMING" ? timing(run, parse(Int, nsteps)) : run_case(run)
    r["run_id"] = id; r["gpu"] = GPU; r["julia"] = string(VERSION); r["threads"] = Threads.nthreads()
    r["waterlily"] = string(pkgversion(WaterLily))
    open(out, "w") do io; JSON.print(io, r); end
end

main(ARGS...)
