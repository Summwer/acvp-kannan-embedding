from fpylll import IntegerMatrix
from g6k.siever import Siever

def store_db(db,filename):
    f = open(filename,"w")
    f.write("%d %d\n" %(len(db),db[0].ncols))
    for i in range(len(db)):
        for j in range(db[i].ncols): 
            f.write(str(db[i][0,j]))
            if(j!=db[i].ncols -1):
                f.write(" ")
        f.write("\n")
    f.close()

def load_db(filename):
    """
    Load db

    """
    try:
        data = open(filename, "r").readlines()
    except FileNotFoundError:
        return None
    data[0] = data[0].split(" ")
    (db_size,dim) = (int(data[0][0]),int(data[0][1]))
    print(db_size,dim)
    db = []
    for i in range(db_size):
        data[i+1] = data[i+1].replace("\n","")
        data[i+1] = data[i+1].split(" ")
        data[i+1] = [int(_) for _ in data[i+1]]
        db.append(data[i+1])
        
    return db


#full sieve on L(B)
def short_vector_sampling_procedure(B):
    g6k = Siever(B, None)
    g6k.lll(0, g6k.full_n)
    n = g6k.full_n
    g6k.shrink_db(0)
    g6k.lll(0, n)
    g6k.initialize_local(0, n- 30, n)

    #generate short vectors by sieving
    while(g6k.r-g6k.l<n):
        g6k()
        g6k.extend_left()
    
    db = list(g6k.itervalues())
    
    print("db_size = %d, db_dim = %d" %(len(db),len(db[0])))
    db_ =[]
    for xv in db:
        db_.append(IntegerMatrix.from_matrix([xv]) * B)
    return db_
