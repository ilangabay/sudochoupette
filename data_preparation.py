import numpy as np
from sklearn.linear_model import LogisticRegression

from sequence_classifier import BasicSequenceClassifier

INITIAL_PROB=[0,0.8,0.15,0.05]

def decide_second(sequence):
    train_source = sequence[:-1]
    last_choice=train_source[-1]
    
    if last_choice==2 :
        probs=[0.1,0,0.6,0.3]
    elif last_choice==3 :
        probs=[0.1,0.6,0,0.3]
    elif last_choice==1 :
        probs=[0,0.6,0.3,0.1]
    elif last_choice==4 :
        probs=[0.2,0.5,0.3,0]
        
    return probs

def decide_third(sequence):
    train_source = sequence[:-1]
    last_choice=train_source[-1]
    probs=[0,0,0,0]
    
    probs[last_choice-1]=0
    if 1 in train_source or 4 in train_source :
        if last_choice==2 :
            probs[2]=0.6
        else :
            probs[1]=0.6
            probs[2]=0.3
        
        if 1 in train_source and 4 not in train_source :
            probs[3]=0.1
            
        elif 4 in train_source and 1 not in train_source :
            probs[0]=0.1
            
        else :
            if max(i for i, x in enumerate(train_source) if x == 4) > max(i for i, x in enumerate(train_source) if x == 1) :
                probs[0]=0.1
                
            else:
                probs[3]=0.1
            
    else :
        probs[3]=0.6
        probs[0]=0.3
        
        if last_choice==2:
            probs[2]=0.1
        else:
            probs[1]=0.1
        
    return probs

def create_train_test(sequence):
    user_input = sequence[-1]
    train_data = []
    full_sequence = sequence[:-1]
    
    # Create sliding windows for training
    for i in range(len(full_sequence) - 5):
        train_data.append(full_sequence[i:i+6])
    
    test_features = full_sequence[-5:]  # Last 5 elements before target
    
    return train_data, test_features, user_input

def count_points(prob_vector, user_input):
    
    sorted_indices = np.argsort(prob_vector)[::-1]
    
    # Convert to 1-based classes (indices 0-3 become classes 1-4)
    ranked_classes = sorted_indices + 1
    
    # Find the position/rank of the user's actual input
    user_rank = np.where(ranked_classes == user_input)[0][0]
    
    # Assign points based on rank (0=1st, 1=2nd, 2=3rd, 3=4th)
    points_mapping = {0: 6, 1: 5, 2: 1, 3: 0}
    
    # print(prob_vector)
    
    return points_mapping[user_rank]

def compare_to_user_input(sequence):
    
    user_input = sequence[-1]
    if len(sequence) == 1:  # Need minimum length
        probs=INITIAL_PROB
        
    elif len(sequence) == 2:
        probs=decide_second(sequence)
    
    elif len(sequence) < 8:
        probs=decide_third(sequence)
        
    else :
        
        
        # Fixed: Create multiple training sequences using sliding window
        train_data = []
        train_source = sequence[:-1]  # Everything except target
        
        for i in range(len(train_source) - 5):
            train_data.append(train_source[i:i+6])
        
        if len(train_data) == 0:
            return 0
            
        clf = BasicSequenceClassifier()
        clf.fit(train_data)  # Now fits multiple sequences
        
        # Fixed: Test features should be last 5 before target
        test = train_source[-5:]  
        probs = clf.predict_proba(test)
    print("probs : ",probs)
    points = count_points(probs, user_input)
    
    return points

def recalculate_average(sequence, current_total, points):
    return (current_total+points)/len(sequence)


def test_compare_to_user_input():
    """Test the complete comparison function."""
    print("\n=== Testing compare_to_user_input function ===")
    
    # Test sequence with pattern
    test_sequence = [1, 2, 3, 4, 1]  # Pattern: 1,2,3,4 repeating, expect 4
    points = compare_to_user_input(test_sequence)
    print(f"Sequence: {test_sequence}")
    print(f"Predicting: {test_sequence[-1]} (actual choice)")
    print(f"Points earned: {points}")
    
    # Test another sequence
    test_sequence_2 = [1, 1, 2, 2, 3, 3, 4, 4]  # Pattern: repeat twice, expect 1
    points_2 = compare_to_user_input(test_sequence_2)
    print(f"\nSequence: {test_sequence_2}")
    print(f"Predicting: {test_sequence_2[-1]} (actual choice)")
    print(f"Points earned: {points_2}")

test_compare_to_user_input()  # Fixed: removed print() wrapper
# print(decide_third([1,3,2,4]))