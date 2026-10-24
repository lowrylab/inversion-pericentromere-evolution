args <- commandArgs(trailingOnly=TRUE)
run_root <- if (length(args)) args[[1]] else "results/maintenance_baseline"
repo_root <- dirname(dirname(normalizePath(run_root, mustWork=FALSE)))
figure_out <- if (length(args) > 1) args[[2]] else file.path(repo_root, "figures", "maintenance_baseline")
out <- file.path(run_root, "analysis")
dir.create(out, recursive=TRUE, showWarnings=FALSE)
dir.create(figure_out, recursive=TRUE, showWarnings=FALSE)
ep <- read.delim(file.path(out, "endpoint_replicates.tsv"), check.names=FALSE)
for (m in sort(unique(ep$mig))) {
  png(file.path(figure_out, sprintf("endpoint_distribution_mig_%g.png", m)), width=1200, height=800, res=140)
  par(mfrow=c(2,2), mar=c(4,4,3,1))
  for (pop in c("p1","p2")) {
    vals <- split(ep, list(ep$model, ep$mig), drop=TRUE)
    inv <- ep[ep$model=="inversion" & ep$mig==m, paste0("A_freq_",pop)]
    per <- ep[ep$model=="permanent_suppression" & ep$mig==m, paste0("A_freq_",pop)]
    boxplot(list(Inversion=inv, Permanent=per), main=paste("A frequency", pop), ylim=c(0,1), ylab="A frequency")
    stripchart(list(Inversion=inv, Permanent=per), vertical=TRUE, method="jitter", add=TRUE, pch=16, col="#333333", cex=.5)
  }
  for (pop in c("p1","p2")) {
    inv <- ep[ep$model=="inversion" & ep$mig==m, paste0("pop_region_copy_burden_",pop)]
    per <- ep[ep$model=="permanent_suppression" & ep$mig==m, paste0("pop_region_copy_burden_",pop)]
    boxplot(list(Inversion=inv, Permanent=per), main=paste("Focal copy burden", pop), ylab="copies")
    stripchart(list(Inversion=inv, Permanent=per), vertical=TRUE, method="jitter", add=TRUE, pch=16, col="#333333", cex=.5)
  }
  mtext(sprintf("Migration = %g", m), outer=TRUE, line=-1.5, cex=1.2)
  dev.off()
}
tr <- read.delim(file.path(out, "trajectory_summary.tsv"), check.names=FALSE)
for (m in c(0, .01, .05)) {
  png(file.path(figure_out, sprintf("trajectory_summary_mig_%g.png", m)), width=1200, height=800, res=140)
  par(mfrow=c(2,2), mar=c(4,4,3,1))
  for (pop in c("p1","p2")) {
    z <- tr[tr$mig==m & tr$pop==pop & tr$metric=="A_freq",]
    plot(NA, xlim=range(z$generation), ylim=c(0,1), xlab="Generation", ylab="A frequency", main=paste("A frequency",pop))
    for (model in c("inversion","permanent_suppression")) { q <- z[z$model==model,]; lines(q$generation,q$mean,col=ifelse(model=="inversion","#1f77b4","#d62728"),lwd=2) }
    legend("topright", legend=c("Inversion","Permanent"), col=c("#1f77b4","#d62728"), lty=1, bty="n")
  }
  for (pop in c("p1","p2")) {
    z <- tr[tr$mig==m & tr$pop==pop & tr$metric=="A_mean_count",]
    plot(NA, xlim=range(z$generation), ylim=range(z$q10,z$q90), xlab="Generation", ylab="A mean focal copies", main=paste("A burden",pop))
    for (model in c("inversion","permanent_suppression")) { q <- z[z$model==model,]; col <- ifelse(model=="inversion","#1f77b4","#d62728"); lines(q$generation,q$mean,col=col,lwd=2); lines(q$generation,q$q10,col=col,lty=3); lines(q$generation,q$q90,col=col,lty=3) }
  }
  mtext(sprintf("Migration = %g", m), outer=TRUE, line=-1.5, cex=1.2)
  dev.off()
}
