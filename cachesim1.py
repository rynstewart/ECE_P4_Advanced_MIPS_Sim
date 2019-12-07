#a. a directly-mapped cache, block size of 16 Bytes, a total of 4 blocks (b=16; N=1; S=4)
#b. a fully-associated cache, block size of 8 Bytes, a total of 8 blocks (b=8; N=8; S=1)
#c. a 2-way set-associative cache, block size of 8 Bytes, 4 sets (b=8; N=2; S=4)

import math

mem_addr=["200c", "2008","2000","2004","201c","2020","2008","2028","200c","2008","2000","2004","201c","2020","2008","2028","2308","2010"]
user_input= input("which case would you like to run a, b, c, d")

def update_LRU(LRU, val): #this function takes the LRU list and the way that is being used now and updating the list
    if val in LRU:
        LRU.insert(0, LRU.pop(LRU.index(val)))
    else:
        LRU.pop()
        LRU.insert(0, val)
    return LRU

def get_least_recently_used(LRU): #this function find the value int LRU that was used least recently
    for i in range(8):
        if (LRU[-(i + 1)] != -1):
            return LRU[-(i + 1)]

if (user_input=='a'):
    blk_size= 16
    total_ways=1
    total_sets=4
    inblk_offset= int(math.log(blk_size,2))
    set_offset= int(math.log(total_sets,2))
    tag=[0 for i in range(4)]
    valid=[0 for i in range(total_sets)]
    Cache=[0 for i in range(64)]
    misses=0
    hits=0

    for i in range (len(mem_addr)):
        address="{0:032b}".format(int(mem_addr[i], 16))                     #get mem addr
        print("Memory address: "+ address)
        set_index= int(address[26:28],2)                                    #get set index
        valid_bit= valid[set_index]                                         #check valid bit
        tag_bits= address[0:26]                                             #get tag bits
        addr_from = hex(int(address[0:32],2) & int("FFFFFFF0",16))          #first address to bring from memory
        addr_to = hex(int(address[0:32],2) | int("F",16))                   #last address to bring from memory

        print("Looking at set/block : "+str(set_index))
        print("Way information: ")
        print("valid bit: " + str(valid_bit))
        print("tag bit:" + str(tag_bits))

        if (valid_bit== 0):                                                     #empty block(miss)
            misses+=1
            valid[set_index]=1                                                  #change the valid bit to 1
            HorM="Miss"
            tag[set_index]= tag_bits                                            #update the tag of the set

        else:                                                                   #valid bit is 1, occupied block
            if(tag[set_index]== tag_bits):                                      #tags match(hit)
                hits+=1
                HorM="Hit"
            else:                                                                #miss due to occupied and new tag
                misses+=1
                HorM="Miss"
                tag[set_index]= tag_bits                                           #update tag for set

        for i in range(16):                                                 #updating Cache
            Cache[(set_index*16)+i]= (hex(int(addr_from,16) +i))

        print("Hit or Miss: "+ HorM)
        print("Memory accessed: M[ " + addr_from + " - " + addr_to+" ]" )
        print("Bringing into block " + str(set_index) + " of the cache\n")

        print("cache: "+ str(Cache)+"\n")


    DM_misses= misses
    DM_hits= hits
    DM_rate= hits/misses

    print("Total hits: " + str(DM_hits))
    print("Total misses: " + str(DM_misses))
    print("Hit rate: " + str(DM_rate))

elif(user_input=='b'):
        ways_tag=[0 for i in range(8)]
        valid=[0 for i in range(8)]
        LRU=[-1 for i in range(8)]
        Cache=[0 for i in range(64)]
        hits=0
        misses=0
        hitway=0
        hit_stat=0
        valid_way=0
        valid_bit=0

        for i in range (len(mem_addr)):
            address="{0:032b}".format(int(mem_addr[i], 16))             #get the address
            print("Memory address: "+ address)
            tag_bits= address[0:29]                                     #get the tag bits of this address
            addr_from = hex(int(address[0:32],2) & int("FFFFFFF8",16))  #first address to bring from memory
            addr_to = hex(int(address[0:32],2) | int("7",16))           #last address to bring from memory

            for i in range(8):                              #check to see if the tag already exist for one of the ways
                if (ways_tag[i] == tag_bits):               #if the tag exists
                    hitway=i                                #save the index of this way which indicates a hit
                    hit_stat=1                              #change stat of hit to 1
                    break
            valid_bit = 1
            for i in range(8):                              #check if any of the ways is empty
                if (valid[i]==0):                           #if so save the index of this way
                    valid_way=i
                    valid_bit=0                             #valid bit of the way is zero
                    break

            if(hit_stat==1):                                #hit since the tags are matching
                print("Looking at set/block : "+str(hitway))
                hits+=1
                LRU = update_LRU(LRU, hitway)               #update LRU since we are using the way
                hit_stat=0                                  #reset
                valid_bit=1
                HorM= "Hit"
                cache_block=hitway
            else:
                misses=+1
                if (valid_bit==0):                          #if the way is empty
                    print("Looking at set/block : "+str(valid_way))
                    ways_tag[valid_way]= tag_bits           #update the tag of the way
                    LRU = update_LRU(LRU, valid_way)        #update LRU
                    valid[valid_way]=1                      #update valid array
                    block_index= valid_way
                    cache_block=valid_way
                else:                                           #if the way is not empty but the tag does not match
                    temp_index = get_least_recently_used(LRU)   #get the least recent used way
                    ways_tag[temp_index]= tag_bits              #update the tag
                    LRU = update_LRU(LRU, temp_index)           #update LRU
                    print("Looking at set/block : "+str(temp_index))
                    block_index= temp_index
                    cache_block=temp_index

                HorM="Miss"


            for i in range(8):                                               #updating Cache
                Cache[(block_index*8)+i]= (hex(int(addr_from,16) +i))       #will add mem[] to load from memory

            print("Way information: ")
            print("valid bit: " + str(valid_bit))
            print("tag bit:" + str(tag_bits))
            print("Hit or Miss: "+ HorM)
            print("Memory accessed: M[ " + addr_from + " - " + addr_to+" ]" )
            print("Bringing into block " + str(cache_block) + " of the cache\n")
            print("cache: "+ str(Cache)+"\n")

        FA_misses= misses
        FA_hits= hits
        FA_rate= hits/misses

        print("Total hits: " + str(FA_hits))
        print("Total misses: " + str(FA_misses))
        print("Hit rate: " + str(FA_rate))

elif(user_input=='c'): #updating cache needs to be fixed

     valid = [[0 for i in range(2)] for j in range(4)]
     ways_tag = [[0 for i in range(2)] for j in range(4)]
     LRU = [[-1 for i in range(2)] for j in range(4)]
     Cache = [0 for i in range(64)]
     hits = 0
     misses = 0
     hit_stat = 0
     valid_way = 0
     valid_bit = 0
     hitway = 0

     for i in range (len(mem_addr)):

         address="{0:032b}".format(int(mem_addr[i], 16))
         print("Memory address: "+ address)
         tag_bits= address[0:27]
         set_index= int(address[27:29],2)
         addr_from = hex(int(address[0:32],2) & int("FFFFFFF8",16))  #first address to bring from memory
         addr_to = hex(int(address[0:32],2) | int("7",16))           #last address to bring from memory

                                                        #in this case we will check four different lists for each sits
         for i in range(2):                             #check to see if the tag already exist for one of the ways
             if (ways_tag[set_index][i] == tag_bits):             #if the tag exists
                 hitway=i                                #save the index of this way which indicates a hit
                 hit_stat=1                              #change stat of hit to 1
                 break
         valid_bit = 1
         for i in range(2):                              #check if any of the ways is empty
             if (valid[set_index][i]==0):                           #if so save the index of this way
                 valid_way=i
                 valid_bit=0                             #valid bit of the way is zero
                 break

         if(hit_stat==1):                                #hit since the tags are matching
             hits+=1
             LRU[set_index] = update_LRU(LRU[set_index], hitway)               #update LRU since we are using the way
             hit_stat=0                                  #reset
             valid_bit=1
             HorM= "Hit"
             print_way=hitway

         else:
             misses+=1
             if (valid_bit==0):                          #if the way is empty
                 ways_tag[set_index][valid_way]= tag_bits           #update the tag of the way
                 LRU[set_index] = update_LRU(LRU[set_index], valid_way)        #update LRU
                 valid[set_index][valid_way]=1                      #update valid array
                 print_way= valid_way

             else:                                           #if the way is not empty but the tag does not match

                 temp_index = get_least_recently_used(LRU[set_index])   #get the least recent used way
                 ways_tag[set_index][temp_index]= tag_bits              #update the tag
                 LRU[set_index] = update_LRU(LRU[set_index], temp_index)           #update LRU
                 print_way= temp_index
             HorM="Miss"

         if(set_index==0):
             for i in range(8):                                               #updating Cache
                 Cache[(print_way*8)+i]= (hex(int(addr_from,16) +i))       #will add mem[] to load from memory
             cache_block=print_way*1

         elif(set_index==1):
             for i in range(8):                                               #updating Cache
                 Cache[((print_way*8)+16)+i]= (hex(int(addr_from,16) +i))       #will add mem[] to load from memory
             cache_block= (print_way*1)+2

         elif(set_index==2):
             for i in range(8):                                               #updating Cache
                 Cache[((print_way*8)+32)+i]= (hex(int(addr_from,16) +i))       #will add mem[] to load from memory
             cache_block= (print_way*1)+4

         elif(set_index==3):
             for i in range(8):                                               #updating Cache
                 Cache[((print_way*8)+48)+i]= (hex(int(addr_from,16) +i))       #will add mem[] to load from memory
             cache_block= (print_way*1)+6
                 


         print("Looking at set: "+str(set_index)+ " ,Way: "+str(print_way))
         print("Way information: ")
         print("valid bit: " + str(valid_bit))
         print("tag bit:" + str(tag_bits))
         print("Hit or Miss: "+ HorM)
         print("Memory accessed: M[ " + addr_from + " - " + addr_to+" ]" )
         print("Bringing into block " + str(cache_block) + " of the cache\n")
         print("cache: "+ str(Cache)+"\n")

         print("\n")

     SA_misses = misses
     SA_hits = hits
     SA_rate = hits / misses

     print("Total hits: " + str(SA_hits))
     print("Total misses: " + str(SA_misses))
     print("Hit rate: " + str(SA_rate))

elif(user_input=='d'):
    
    valid = [[0 for i in range(4)] for j in range(2)]
    ways_tag = [[0 for i in range(4)] for j in range(2)]
    LRU = [[-1 for i in range(4)] for j in range(2)]
    Cache = [0 for i in range(64)]
    hits = 0
    misses = 0
    hit_stat = 0
    valid_way = 0
    valid_bit = 0
    hitway = 0
    cache_block=0

    
    for i in range (len(mem_addr)):
        
        address="{0:032b}".format(int(mem_addr[i], 16))
        print("Memory address: "+ address)
        tag_bits= address[0:28]
        set_index= int(address[28:29],2)
        addr_from = hex(int(address[0:32],2) & int("FFFFFFF8",16))  #first address to bring from memory
        addr_to = hex(int(address[0:32],2) | int("7",16))           #last address to bring from memory

                                                    #in this case we will check four different lists for each sits
        for i in range(4):                             #check to see if the tag already exist for one of the ways
            
            if (ways_tag[set_index][i] == tag_bits):             #if the tag exists
                hitway=i                                #save the index of this way which indicates a hit
                hit_stat=1                              #change stat of hit to 1
                break
        valid_bit = 1

        for i in range(4):                              #check if any of the ways is empty
            if (valid[set_index][i]==0):                           #if so save the index of this way
                valid_way=i
                valid_bit=0                             #valid bit of the way is zero
                break
            
        if(hit_stat==1):                                #hit since the tags are matching
            hits+=1
            LRU[set_index] = update_LRU(LRU[set_index], hitway)               #update LRU since we are using the way
            hit_stat=0                                  #reset
            valid_bit=1
            HorM= "Hit"
            print_way=hitway

        else:
            misses+=1
            if (valid_bit==0):                          #if the way is empty
                ways_tag[set_index][valid_way]= tag_bits           #update the tag of the way
                LRU[set_index] = update_LRU(LRU[set_index], valid_way)        #update LRU
                valid[set_index][valid_way]=1                      #update valid array
                print_way= valid_way

            else:                                           #if the way is not empty but the tag does not match

                temp_index = get_least_recently_used(LRU[set_index])   #get the least recent used way
                ways_tag[set_index][temp_index]= tag_bits              #update the tag
                LRU[set_index] = update_LRU(LRU[set_index], temp_index)           #update LRU
                print_way= temp_index
            HorM="Miss"
            
        if(set_index==0):
            for i in range(8):                                               #updating Cache
                Cache[(print_way*8)+i]= (hex(int(addr_from,16) +i))       #will add mem[] to load from memory
            cache_block=print_way*1

        elif(set_index==1):
            for i in range(8):           #updating Cache
                Cache[((print_way*8)+32)+i]= (hex(int(addr_from,16) +i))       #will add mem[] to load from memory
            cache_block= (print_way*1)+4
                 



        print("Looking at set: "+str(set_index)+ " ,Way: "+str(print_way))
        print("Way information: ")
        print("valid bit: " + str(valid_bit))
        print("tag bit:" + str(tag_bits))
        print("Hit or Miss: "+ HorM)
        print("Memory accessed: M[ " + addr_from + " - " + addr_to+" ]" )
        print("Bringing into block " + str(cache_block) + " of the cache\n")
        print("cache: "+ str(Cache)+"\n")

        print("\n")

    SA_misses = misses
    SA_hits = hits
    SA_rate = hits / misses

    print("Total hits: " + str(SA_hits))
    print("Total misses: " + str(SA_misses))
    print("Hit rate: " + str(SA_rate))











    
