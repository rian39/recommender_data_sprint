library(RedditExtractoR)

setwd("/home/rja/VOSON/other_projects/2019/DataSprint/Reddit")

subreddits <- read.csv("subreddits.csv", stringsAsFactors=F, header=F, comment.char = "#")

#subreddits <- subreddits[which(subreddits$V1=="gameofthrones"),]

date_t <- format(Sys.time(), "%Y-%m-%d_%H:%M")
data_dir <- "data2"

for (s in subreddits[,2]){

    #cat("Working on:",s,"\n")
    #next
    
    urls <- read.csv(paste0("urls/",s,".csv"), stringsAsFactors=F, header=F)
    print(urls)

    system(paste0("mkdir -p ",data_dir,"/",s))
    for (i in urls$V1){
        post <- gsub(".+/comments/(.+?)/.+", "\\1", i, perl = TRUE)
        print(post)

        example_attr <- reddit_content(URL=i)

        write.csv(example_attr,paste0(data_dir,"/",s,"/data_",post,".",date_t,".csv"))
        
    }
    
}


