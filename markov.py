import sys
import random 
import string
import os
import twitter

api = twitter.Api(
        consumer_key = os.environ["TWITTER_CONSUMER_KEY"],
        consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"],
        access_token_key = os.environ["TWITTER_ACCESS_TOKEN_KEY"],
        access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
        )

class SimpleMarkovGenerator(object):

    def __init__(self, filenames):
        self.filenames = filenames

    def read_files(self):
        """Given a list of files, make chains from them."""
        result = []
        for f in self.filenames:
            text_file = open(f).read()
            corpus = text_file.split()
            result += corpus
        self.result = result
        return self


    def make_chains(self, n=2):
        """Takes input text as string; stores chains."""

        # your code here
        length_full_text = len(self.result)-n
        ngrams = {}
        for i in range(length_full_text):
            pre_tup = []
            for j in range(n):
                pre_tup.append(self.result[i+j])
            tup = tuple(pre_tup)
            ngrams.setdefault(tup,[]).append(self.result[i+n])

        return ngrams

    def make_text(self, chains, n=2):
        """Takes dictionary of markov chains; returns random text."""

        # your code here
        start = random.choice(chains.keys())
        while start[0][0].isupper()== False or start[0][-1] in string.punctuation:
            start = random.choice(chains.keys())
        first_word = list(start[-(n-1):]) 
        next = random.choice(chains[start])
        result = list(start)

        result.append(next)


        while next[-1] != "." and next[-1]!= "?" and next[-1]!= "!"  :
            new = tuple(first_word+[next]) #should be list converted to tuple--make sure it create n tuple
            next_word = random.choice(chains[new]) #check to see if changing variable "next" works
            result.append(next_word)
            first_word = result[-n:-1] #first_word returns n-1 words
            next = result[-1]


        return " ".join(result)
 
# Create a TweetableMarkovGenerator. 
# This should subclass your Markov generator, 
# but will need to either override or add a method 
# to make the output less than 140 characters (
# or it could add an attribute and you could 
# change a method in the base class methods;
# there are lots of different ways you could solve this problem!)

# class UpperMixin(object):
#     def uppercase(self):
#         self = self.upper()
#         return self



class TweetableMarkovGenerator(SimpleMarkovGenerator):
    def make_text(self, chains, n=2):
        evalu = super(TweetableMarkovGenerator, self).make_text(chains, n=2)
        while len(evalu) > 140:
             evalu = super(TweetableMarkovGenerator, self).make_text(chains, n=2)
        return evalu


        


if __name__ == "__main__":

    # we should get list of filenames from sys.argv
    functions = sys.argv[0]
    text = sys.argv[1:]
    
    # we should make an instance of the class
    generator1 = TweetableMarkovGenerator(text)
    # we should call the read_files method with the list of filenames
    chain_dict = generator1.read_files().make_chains()

    # we should call the make_text method 5x
    # for i in range(1):
    #     print generator1.make_text(chain_dict)
    # pass

print api.VerifyCredentials()

status = api.PostUpdate(generator1.make_text(chain_dict))
print status.text