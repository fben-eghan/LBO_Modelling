RealEstateInvestment <- function(p=1e6, e=0.25, r=0.06, lt=10, ap=25, agr=0.02, arg=0.02,
ecr=0.08, ih=5, irr=0.15, ri=5e4, ex=2.5e4, t=0.2) {
d <- pe
e <- (1 - e)p
pmt <- -pmt(r/12, lt12, -d, 0)
noi <- ri - ex
iters <- 10000
p_dist <- rnorm(iters, p, 0.05p)
ri_dist <- rnorm(iters, ri, 0.05ri)
ex_dist <- rnorm(iters, ex, 0.05ex)
agr_dist <- rnorm(iters, agr, 0.05agr)
arg_dist <- rnorm(iters, arg, 0.05arg)
ecr_dist <- rnorm(iters, ecr, 0.05*ecr)
irr_dist <- rep(0, iters)

calculate <- function(num_sims=10000, ...) {
for (key in names(list(...))) {
assign(key, list(...)[[key]], envir = .GlobalEnv)
}
res <- rep(0, num_sims)
for (i in seq_len(num_sims)) {
d <<- pe
e <<- (1 - e)p
pmt <<- -pmt(r/12, lt12, -d, 0)
noi <<- ri - ex
annual_cash_flow_before_tax <- noi - (rd + pmt)*12
annual_cash_flow_after_tax <- annual_cash_flow_before_tax * (1 - t)
terminal_value <- annual_cash_flow_before_tax * (1 + arg) / (ecr - arg)
cash_flows <- c(-e, rep(annual_cash_flow_after_tax, ih), terminal_value)
irr_dist[i] <<- IRR(cash_flows)
res[i] <- ifelse(irr_dist[i] >= irr, 1, 0)
}
return(sum(res) / num_sims)
}
return(list(p=p, e=e, r=r, lt=lt, ap=ap, agr=agr, arg=arg, ecr=ecr, ih=ih, irr=irr, ri=ri, ex=ex, t=t,
d=d, pmt=pmt, noi=noi, iters=iters, p_dist=p_dist, ri_dist=ri_dist, ex_dist=ex_dist,
agr_dist=agr_dist, arg_dist=arg_dist, ecr_dist=ecr_dist, irr_dist=irr_dist, calculate=calculate))
}

assuming you have already instantiated the RealEstateInvestment class and defined the calculate method

num_sims <- 10000
results <- replicate(num_sims, RealEstateInvestment()$calculate(num_sims))

library(ggplot2)
ggplot() +
geom_histogram(aes(x=results), binwidth = 0.01, fill="skyblue", color="black", alpha=0.8) +
geom_density(aes(x=results), color="red", size=2) +
labs(x="IRR Probability", y="Density", title="Distribution of IRR Probability") +
theme_minimal()
