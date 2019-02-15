library(igraph)
library(tidyr)
library(networkD3)

data_dir_t <- "data2"

subred <- "mens-rights"
#subred <- "KotakuInAction"
data_dir <- paste0(data_dir_t,"/",subred)

system(paste0("mkdir -p networks/",subred))

files_t <- list.files(data_dir)

targ <- "apo5sj"                             #should pick this up from the urls file...
thread_starter <- "Economy_Cactus"           #should pick up programmatically

g <- graph.empty(0, directed=TRUE)
g <- make_empty_graph(directed=TRUE) %>% add_vertices(1, name = "0", user=thread_starter, time=1)
n_prev <- 0
t <- 1
for (i in grep(targ,files_t)){

    df <- read.csv(paste0(data_dir,"/",files_t[i]), stringsAsFactors=F)
    #print(nrow(df))
    #print(head(df))

    if ( nrow(df) <= n_prev )           #no new data
        next
    
    cat("working on:", files_t[i], "\n")

    df_t <- df[,which(colnames(df) %in% c("id","structure","user"))]

    #connect top-level post to thread start (better way of doing this)
    #ind <- which(!grepl("_",df_t$structure))
    #df_t$structure[ind] <- paste0("0_",df_t$structure[ind])
    df_t$structure2 <- paste0("0_",df_t$structure)
    
    df_t2 <- extract(df_t, structure2, into = c('parent', 'child'), '(.*)_(\\d+)$', remove=F)

    for (j in 1:nrow(df_t2)){
        print(df_t2$structure[j])
        if (length(which(V(g)$name==df_t2$structure2[j]))==0){
            g <- add_vertices(g, 1, name=df_t2$structure2[j], user=df_t2$user[j], time=t)
            g <- add_edges(g, c(vcount(g),which(V(g)$name==df_t2$parent[j])))
        }
    }

    V(g)$label <- V(g)$user
    V(g)$color <- rainbow(t)[V(g)$time]

    png(paste0("networks/",subred,"/net_",targ,"_igraph_",t,".png"), width=800, height=700)
    plot(g, directed = TRUE, direction = "climb")
    dev.off()

    dd <- igraph_to_networkD3(g)
    dd$nodes$user <- V(g)$user
    dd$nodes$time <- V(g)$time

    fdn <- forceNetwork(Links = dd$links, Nodes = dd$nodes,
                        Source = 'source', Target = 'target', NodeID = 'user',
                        Group = 'time')

    #seems to need full path
    fn <- paste0(getwd(),"/networks/",subred,"/net_",targ,"_networkD3_",t,".html")
    #print(fn)
    saveNetwork(fdn, file = fn)

    #copy relevant data file
    cmd <- paste0("cp ",data_dir,"/",files_t[i]," networks/",subred)
    #print(cmd)
    system(cmd)
    
    t <- t+1
    n_prev <- nrow(df)
}
t <- t-1

V(g)$label <- V(g)$user
V(g)$color <- rainbow(t)[V(g)$time]

plot(g, directed = TRUE, direction = "climb")

#force-directed with networkD3
#wc <- cluster_walktrap(g)
#members <- membership(wc)

#seems needs group for forceNetwork...can use time of post?
#dd <- igraph_to_networkD3(g, group=members)
dd <- igraph_to_networkD3(g)
dd$nodes$user <- V(g)$user
dd$nodes$time <- V(g)$time

fdn <- forceNetwork(Links = dd$links, Nodes = dd$nodes,
            Source = 'source', Target = 'target', NodeID = 'user',
            Group = 'time')

saveNetwork(fdn, file = 'Net1.html')

#for radialNetwork, need list object
#use data.tree for conversion
df3 <- data.frame(Parent=head_of(g,E(g))$user, Child=tail_of(g,E(g))$user)

library('data.tree')
#for larger network, getting error on this: 
#Error: C stack usage  7970020 is too close to the limit
tree <- FromDataFrameNetwork(df3)
tree
lol <- ToListExplicit(tree, unname = TRUE)
diagonalNetwork(lol)
radialNetwork(List = lol, fontSize = 10, opacity = 0.9)
