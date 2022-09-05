class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        # add winning conditions, grab winning address, post to blockchain
        if p1 == "R" and p2 == "S":
            winner = 0
            winner_addr = user1_algo_addr
            loser_uid = user2_uid
        elif p1 == "S" and p2 == "R":
            winner = 1
            winner_addr = user2_algo_addr
            loser_uid = user1_uid
        elif p1 == "P" and p2 == "R":
            winner = 0
            winner_addr = user1_algo_addr
            loser_uid = user2_uid
        elif p1 == "R" and p2 == "P":
            winner = 1
            winner_addr = user2_algo_addr
            loser_uid = user1_uid
        elif p1 == "S" and p2 == "P":
            winner = 0
            winner_addr = user1_algo_addr
            loser_uid = user2_uid
        elif p1 == "P" and p2 == "S":
            winner = 1
            winner_addr = user2_algo_addr
            loser_uid = user1_uid
        note = "Player 1 chose {0} and player 2 chose {1}.".format(p1,p2)
        payout_winner(app_id, loser_uid, winner_addr, note)
        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
	
# [ Start DropChain API Integrations ]
import requests, json

# grabbed from DropChain test user accounts
user1_uid = "<your Test User ID 1>" # test user uid 1 
user2_uid = "<your Test User ID 2>" # test user uid 2  
user1_algo_addr = "<your Algo Address Test User 1>" # test user 1 algorand addr
user2_algo_addr = "<your Algo Address Test User 2>" # test user 2 algorand addr
app_id = "<your App ID>" # app_id 

# The entire function is taken from RapidAPI's Python "request" example. 
# It takes in inputs from above (that you would customize in the event of your game) 
# and conducts a DropChain API call for your players.
run_count = 0

def payout_winner(app_id, user1_uid, winner_addr, note): 

    url = "https://dropchain1.p.rapidapi.com/dropchain/v1/send_algo"

    payload = {
	"app_id": app_id,
        "user1_uid": user1_uid,
        "receiver1_address": winner_addr,
        "asset1_amount_int": "100000", # this amount can be changed based on the wager for the game
        "transaction1_note": note
    }
    headers = {
	    "content-type": "application/json",
	    "X-RapidAPI-Key": "<your RapidAPI account Key>", # taken from your RapidAPI account
	    "X-RapidAPI-Host": "dropchain1.p.rapidapi.com"
    }

    # ensure function runs 1 time — fixes demo when winner() is called multiple times
    global run_count
    if run_count == 0:
        response = requests.request("POST", url, json=payload, headers=headers)
        run_count += 1
        response_dict = json.loads(response.text)
        return response_dict
    else:
        return

# [ End DropChain API Integrations ]
