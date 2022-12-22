import numpy as np
import math
# generate 10 samples with different preference
class generateSet:
    def __init__(self,numOfPerson=10000,numOfMAB=10,number_he_like=10,method='random',reward_method = 'more than'):
        self.person = numOfPerson
        self.number_he_like = number_he_like
        self.MAB = numOfMAB
        self.preference = np.zeros((numOfPerson, numOfMAB))
        self.preference_pred = np.zeros((numOfPerson, numOfMAB))
        self.randPreference(method)
        self.preference_pred = self.randPreference_pred()
        self.sparse = 0.8   # may not click the content that did attract user
        self.reward_method = reward_method

    def randPreference_pred(self):
        preference = np.zeros((self.person, self.MAB))
        for i in range(self.person):
            for j in range(self.MAB):
                mynum = np.random.randint(-1,1) * np.random.randint(10,60)/100
                preference[i,j] = self.preference[i,j] + mynum
                x=1
        for i in range(self.person):
            for j in range(self.MAB):
                if preference[i,j] < 0:
                    preference[i, j] = 0
                if preference[i,j] > 1:
                    preference[i, j] = 0.99
        # print('preference',self.preference)
        # print('Preference_pred',preference)
        return preference

    def randPreference(self,method = 'random'):
        if method == 'random':
            for i in range(self.person):
                for j in range(self.MAB):
                    self.preference[i, j] = np.random.rand()
        elif method == 'like&hate':
            for i in range(self.person):
                index_like = np.random.randint(1, self.MAB,[1,self.number_he_like])
                for j in range(self.number_he_like):
                    self.preference[i,index_like[0][j]] = np.random.randint(math.floor(0.9*self.MAB*10),self.MAB*10)/(self.MAB*10)
        elif method == 'like&ok':
            for i in range(self.person):
                index_like = np.random.randint(1, self.MAB, [1, self.number_he_like])
                for j in range(self.number_he_like):
                    self.preference[i, index_like[0][j]] = np.random.randint(math.floor(0.9 * self.MAB * 10),
                                                                             self.MAB * 10) / (self.MAB * 10)
                for j in range(self.MAB):
                    if self.preference[i, j] == 0:
                        self.preference[i, j] = np.random.randint(1, math.floor(0.9 * self.MAB * 10)) / (self.MAB * 10)
        else:
            for i in range(self.person):
                for j in range(self.MAB):
                    self.preference[i, j] = np.random.rand()

    def renew_preference(self):
        pass

    def doULike(self,xthPerson=1,xthMAB=1):
        if np.random.rand() > self.preference[xthPerson,xthMAB]:
            return -1
        else:
            return 1

    def step(self,person_choose,s,action,actions_value,reward_method='more than'):
        reward=0
        reward_method = self.reward_method
        # cosine similarity:
        actions_value = np.array(actions_value).flatten()
        # print('actions_value111111',actions_value)
        # print('np.min(a)',np.min(actions_value))
        if np.min(actions_value)<0:
            actions_value = actions_value - np.min(actions_value)
        # print('actions_value22222',actions_value)
        # print('sum11111',np.sum(actions_value))
        actions_value = actions_value/np.sum(actions_value)

        s = np.array(s).flatten()
        if reward_method == 'cosine_linear':
            cosine_similarity = np.dot(np.exp(actions_value),np.exp(np.exp(s)))/(np.linalg.norm(np.exp(actions_value), 2) * np.linalg.norm(np.exp(np.exp(s)), 2))
            np.exp(actions_value)

            # todo: regularize
            reward = cosine_similarity
            # print('reward:',reward)
        elif reward_method == 'cosine_exp':
            cosine_similarity = np.dot(actions_value,s)/(np.linalg.norm(actions_value, 2) * np.linalg.norm(s, 2))
            # cosine_similarity = np.dot(np.exp(actions_value),np.exp(s*10))/(np.linalg.norm(actions_value, 2) * np.linalg.norm(s, 2))
            # cosine_similarity = np.dot(np.exp(np.exp(actions_value)),np.exp(np.exp(s)))/(np.linalg.norm(np.exp(np.exp(actions_value)), 2) * np.linalg.norm(np.exp(np.exp(s)), 2))

            # todo: regularize
            # reward = (1.6-np.exp(cosine_similarity))*8#3*max(actions_value)
            reward = (np.exp(cosine_similarity)-0)*8#3*max(actions_value)
            #reward = cosine_similarity
            # print('reward:11111111',reward)
            # print('actions_value:11111111',actions_value)
            # print('s:11111111',s)
        elif reward_method == 'real':
            # print('self.preference[person_choose, action]*100',self.preference[person_choose, action]*100)
            # print('proba',math.ceil(self.preference[person_choose, action]*100))
            reward = np.random.randint(-1,math.ceil(self.preference[person_choose, action]*100))
            reward = np.exp(reward/100)
            # print('reward',reward)

            cosine_similarity=0

        elif reward_method == 'more than':
            for i in range(self.MAB):
                if i != action:
                    if self.preference[person_choose,i]<self.preference[person_choose,action]:
                        reward+=1

            cosine_similarity = 0
        else:
            print('reward_method error')
            cosine_similarity = 0
        self.state_renew(person = person_choose,action = action,reward = reward)
        return reward,cosine_similarity,actions_value

    def state_renew(self,person,action,reward):
        # print('reward',reward-1.3)
        # print("###########################")
        # print(self.preference_pred[person, :])
        self.preference_pred[person,action] += (reward-1.3)*0.1

        # print(self.preference_pred[person, :])
        # print(self.preference[person, :])
        if self.preference_pred[person,action]< 0:
            self.preference_pred[person, action] = 0
        if self.preference_pred[person,action]>10:
            self.preference_pred[person, action] = 0.99
