do_wavelet = function(numlevel,filtername, bdd,filename){
	library(wavelets)
	#file.remove(filename)
	ECG = read.table("/home/hansjung/바탕화면/temp/ECG.csv",sep = ",")
	for(i in 1:nrow(ECG)){
		temp = ECG[i,]
		temp = temp[1:8192]
		patient = as.numeric(unlist(temp))
		wt = dwt(patient, filter = filtername, n.levels = numlevel, boundary = bdd, fast = TRUE)
		jiyeon = wt@W[numlevel]
		jiyeon = jiyeon[1]
		jiyeon = c(do.call("cbind",jiyeon))
		jiyeon = t(jiyeon)
		#jiyeon = t(jiyeon)
		#write.csv(jiyeon, file = "result.csv", append=TRUE)
		write.table(jiyeon, file = filename, sep = ",", col.names = FALSE, append=TRUE, qmethod = c("escape", "double"), eol = "\n")
		#write(jiyeon,file = "result.txt",sep = ",", append = TRUE)
	}
}