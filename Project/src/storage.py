
def store_sequences(list_of_sequences, rank):
    if len(list_of_sequences):
        with open("./data_thread_{0}.data".format(rank), "a") as f:
            for x in list_of_sequences:
                f.write(str(x) + "\n")
