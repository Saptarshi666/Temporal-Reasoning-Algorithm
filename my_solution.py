def main():
    f = open("state_weights.txt","r")
    test1 = f.readline()
    line = f.readline()
    cord = line.split()
    num_states = int(cord[0])
    state_info_from_state_weight = []
    weight_info_from_state_weight = []
    i = 0
    while i < num_states:
        line = f.readline()
        cord = line.split()
        state_info_from_state_weight.append(cord[0])
        weight_info_from_state_weight.append(float(cord[1]))
        i = i + 1
    f.close()
    f = open("state_action_state_weights.txt","r")
    test1 = f.readline()
    line = f.readline()
    cord = line.split()
    num_of_triplets = int(cord[0])
    num_of_actions = int(cord[2])
    state_action_state_weight_info = float(cord[3])
    i = 0
    Dict_data_from_state_action_state = {}
    while i < num_of_triplets:
        line = f.readline()
        cord = line.split()
        if cord[1] not in Dict_data_from_state_action_state:
            Dict_final_data = {}
            Dict_final_data[cord[2]] = int(cord[3])
            Dict_final_data_with_initial_state = {}
            Dict_final_data_with_initial_state[cord[0]] = Dict_final_data
            Dict_data_from_state_action_state[cord[1]] = Dict_final_data_with_initial_state
        else:
            Dict_final_data_with_initial_state = Dict_data_from_state_action_state[cord[1]]
            if cord[0] not in Dict_final_data_with_initial_state:
                Dict_final_data = {}
                Dict_final_data[cord[2]] = int(cord[3])
                Dict_final_data_with_initial_state[cord[0]] = Dict_final_data
            else:
                Dict_final_data = Dict_final_data_with_initial_state[cord[0]]
                Dict_final_data[cord[2]] = int(cord[3])
        i = i + 1
    f.close()
    a = 0
    for key in Dict_data_from_state_action_state:
        Dict_final_data_with_initial_state = Dict_data_from_state_action_state[key]
        for key1 in Dict_final_data_with_initial_state:
            Dict_final_data = Dict_final_data_with_initial_state[key1]        
            total = sum(Dict_final_data.values()) + ((num_states - len(Dict_final_data))*state_action_state_weight_info)
            Dict_final_data = {k: v / total for k, v in Dict_final_data.items()}
            if num_states > len(Dict_final_data) :
                Dict_final_data["Missing"] = state_action_state_weight_info/total
            Dict_final_data_with_initial_state[key1] = Dict_final_data
        Dict_data_from_state_action_state[key] = Dict_final_data_with_initial_state
    
    f = open("state_observation_weights.txt","r")
    test1 = f.readline()
    line = f.readline()
    cord = line.split()
    num = int(cord[0])
    num_of_observation = int(cord[2])
    state_observation_weight_info = float(cord[3])
    i = 0
    Dict_data_from_state_observation = {}
    while i < num:
        line = f.readline()
        cord = line.split()
        if cord[0] not in Dict_data_from_state_observation:
            Dict_final_data = {}
            Dict_final_data[cord[1]] = int(cord[2])
            Dict_data_from_state_observation[cord[0]] = Dict_final_data
        else:
            Dict_final_data= Dict_data_from_state_observation[cord[0]]
            Dict_final_data[cord[1]] = int(cord[2])
        i = i + 1
    f.close()
    for key in Dict_data_from_state_observation:
        Dict_final_data = Dict_data_from_state_observation[key]
        total = sum(Dict_final_data.values()) + ((num_of_observation-len(Dict_final_data))*state_observation_weight_info)
        Dict_final_data = {k: v / total for k, v in Dict_final_data.items()}
        Dict_final_data["Missing"] = state_observation_weight_info/total
        Dict_data_from_state_observation[key] = Dict_final_data

    f = open("observation_actions.txt","r")
    test1 = f.readline()
    line = f.readline()
    cord = line.split()
    num = int(cord[0])
    observation_info_from_observation_action = []
    actions_info_from_observation_action = []
    observation_set = set()
    observation_array = []
    action_array = []
    i = 0
    while i < num:
        line = f.readline()
        cord = line.split()
        observation_info_from_observation_action.append(cord[0])
        observation_array.append(cord[0])
        observation_set.add(cord[0])
        if 1 < len(cord):
            actions_info_from_observation_action.append(cord[1])
            action_array.append(cord[1])
        else:
            actions_info_from_observation_action.append("")
            action_array.append("")
        i = i + 1
    for key in Dict_data_from_state_action_state:
        Dict_final_data_with_initial_state = Dict_data_from_state_action_state[key]
        for state in state_info_from_state_weight:
            if state not in Dict_final_data_with_initial_state:
                Dict_final_data_with_initial_state[state] =  1/num_states
        Dict_data_from_state_action_state[key] = Dict_final_data_with_initial_state
    if num_of_actions > len(Dict_data_from_state_action_state):
        Dict_data_from_state_action_state["Missing"] = 1/num_states
    for state in state_info_from_state_weight:
        if state not in Dict_data_from_state_observation:
            Dict_data_from_state_observation[state] = 1/num_of_observation
    f.close()
    #normalize state weights
    key_count = 0
    total = sum(weight_info_from_state_weight)
    weight_info_from_state_weight = [x/total for x in weight_info_from_state_weight]
    trellis = [[0 for i in range(len(observation_array)) ] for j in range(len(state_info_from_state_weight))]
    pointers = [[0 for i in range(len(observation_array)) ] for j in range(len(state_info_from_state_weight))]
    for s in range(len(state_info_from_state_weight)):
        state = state_info_from_state_weight[s]
        val = -9
        if state in Dict_data_from_state_observation:
            Dict= Dict_data_from_state_observation[state]
            if observation_array[0] in Dict:
                val = Dict[observation_array[0]]
            else:
                val = Dict["Missing"]
        else:
            val = Dict_data_from_state_observation["Missing"]
        trellis[s][0]= weight_info_from_state_weight[s] * val
    for o in range(1,len(observation_array)):
        action = action_array[o-1]   
        for s in range(len(state_info_from_state_weight)):
            j = -5
            best = float(-9)
            state = state_info_from_state_weight[s]
            emission = -9
            if state in Dict_data_from_state_observation:
                Dict= Dict_data_from_state_observation[state]
                if observation_array[o] in Dict:
                    emission = Dict[observation_array[o]]
                else:
                    emission = Dict["Missing"]
            else:
                emission = Dict_data_from_state_observation["Missing"]
            for k in range(len(state_info_from_state_weight)):
    
                trellis_val = trellis[k][o-1]
                transition = -9      
                state = state_info_from_state_weight[k]
                Dict_final_data_with_initial_state = Dict_data_from_state_action_state[action]
                if action in Dict_data_from_state_action_state:
                    if state in Dict_final_data_with_initial_state:
                        final_state = state_info_from_state_weight[s]
                        Dict_final_data = Dict_final_data_with_initial_state[state]
                        if final_state in Dict_final_data:
                            transition = Dict_final_data[final_state]
                        else:
                            transition = Dict_final_data["Missing"]
                    else:
                        transition = Dict_final_data_with_initial_state["Missing"]
                else:
                    transition = Dict_data_from_state_action_state["Missing"]
                val_check = trellis_val * transition * emission
                if val_check > best:
                    best = val_check
                    j = k
            trellis[s][o] = best
            pointers[s][o] = j       
    best_path = []
    j = -9
    best = -9
    for k in range(len(state_info_from_state_weight)):
        if trellis[k][len(observation_array)-1] > best:
            best = trellis[k][len(observation_array)-1]
            j = k
    for o in range(len(observation_array)-1,-1,-1):
        best_path.append(state_info_from_state_weight[j])
        j = pointers[j][o]          
    with open('states.txt', 'w') as f:
        f.write('states\n')
        f.write(str(len(best_path)) + '\n')
        for state in reversed(best_path):
            f.write(state + '\n')

                                













if __name__ == "__main__":  
    main()