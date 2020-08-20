import random
import tkinter


def create_top_frame():
    result_frame = tkinter.Frame(main_window, background="green")
    result_frame.grid(row=0, column=2, columnspan=2, sticky="we")
    result_text = tkinter.StringVar()
    result_label = tkinter.Label(result_frame, background="green", textvariable=result_text)
    result_label.config(font=("Courier", 30))
    result_label.grid(row=0, column=0, sticky="we")
    return result_text


def create_card_frame():
    card_frame = tkinter.Frame(main_window, background="green")
    card_frame.grid(row=1, column=1, columnspan=4, rowspan=4, sticky="wens")

    ######################################################################################
    dealer_frame = tkinter.Frame(card_frame, background="green")
    dealer_frame.grid(row=0, column=0, columnspan=4)

    tkinter.Label(main_window, text="Dealer", background="green").grid(row=1, column=0, sticky="nswe")
    dealer_score_var = tkinter.IntVar()
    dealer_score_label = tkinter.Label(main_window, textvariable=dealer_score_var, background="green")
    dealer_score_label.grid(row=2, column=0, sticky="nswe")
    ######################################################################################
    player_frame = tkinter.Frame(card_frame, background="green")
    player_frame.grid(row=1, column=0, columnspan=4)

    tkinter.Label(main_window, text="Player", background="green").grid(row=3, column=0, sticky="nswe")
    player_score_var = tkinter.IntVar()
    player_score_label = tkinter.Label(main_window, textvariable=player_score_var, background="green")
    player_score_label.grid(row=4, column=0, sticky="nswe")

    return tuple((dealer_frame, dealer_score_var, player_frame, player_score_var, card_frame))


def create_button_frame():
    button_frame = tkinter.Frame(main_window, background="green")
    button_frame.grid(row=5, column=0, columnspan=3, sticky="we")

    dealer_button = tkinter.Button(button_frame, text="Dealer", command=deal_dealer)
    dealer_button.grid(row=0, column=0)

    player_button = tkinter.Button(button_frame, text="Player", command=deal_player)
    player_button.grid(row=0, column=1)

    new_game_button = tkinter.Button(button_frame, text="New Game", command=new_game)
    new_game_button.grid(row=0, column=3)


def create_scoreboard():
    scoreboard_frame = tkinter.LabelFrame(main_window, text="Scoreboard")
    scoreboard_frame.grid(row=2, column=5)

    dealer_wins = tkinter.IntVar()
    dealer_wins_label = tkinter.Label(scoreboard_frame, text="Dealer wins")
    dealer_wins_label.grid(row=0, column=0)
    dealer_scoreboard = tkinter.Label(scoreboard_frame, textvariable=dealer_wins)
    dealer_scoreboard.grid(row=1, column=0)

    player_wins = tkinter.IntVar()
    player_wins_label = tkinter.Label(scoreboard_frame, text="player wins")
    player_wins_label.grid(row=2, column=0)
    player_scoreboard = tkinter.Label(scoreboard_frame, textvariable=player_wins)
    player_scoreboard.grid(row=3, column=0)

    return tuple((dealer_wins, player_wins))


def new_game():
    global shuffled_cards
    global end_of_round

    end_of_round = False
    for frame in in_game_cards_frames:
        frame.destroy()
    result_value.set("")
    player_hand.clear()
    dealer_hand.clear()

    shuffled_cards = list(cards)
    random.shuffle(shuffled_cards)

    deal_player()
    dealer_hand.append(deal_card(dealer_main_frame))
    dealer_score_value.set(count_score(dealer_hand))
    deal_player()


def load_cards(card_list):
    suits = ["heart", "club", "diamond", "spade"]
    face_cards = ["jack", "queen", "king"]
    extension = "png"
    for suit in suits:
        for i in range(1, 11):
            name = "cards\\{}_{}.{}".format(i, suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_list.append((i, image))

        for card in face_cards:
            name = "cards\\{}_{}.{}".format(card, suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_list.append((10, image))


def deal_card(frame):
    picked_card = shuffled_cards.pop()
    card_frame = tkinter.Label(frame, image=picked_card[1])
    card_frame.pack(side="left")
    in_game_cards_frames.append(card_frame)

    return picked_card


def count_score(hand):
    score = 0
    ace = False
    for card in hand:
        card_value = card[0]

        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value

        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def deal_dealer():
    global dealer_points
    global player_points
    global end_of_round
    score = count_score(dealer_hand)
    while 0 < score < 17:
        card = deal_card(dealer_main_frame)
        dealer_hand.append(card)
        score = count_score(dealer_hand)
        dealer_score_value.set(score)

    player_score = count_score(player_hand)
    if player_score > 21:
        result_value.set("Dealer wins!")
        if not end_of_round:
            end_of_round = True
            dealer_points += 1
            dealer_pointing.set(dealer_points)
    elif score > 21 or score < player_score:
        result_value.set("Player wins!")
        if not end_of_round:
            end_of_round = True
            player_points += 1
            player_pointing.set(player_points)
    elif score > player_score:
        result_value.set("Dealer wins!")
        if not end_of_round:
            end_of_round = True
            dealer_points += 1
            dealer_pointing.set(dealer_points)
    else:
        result_value.set("Draw!")
        end_of_round = True


def deal_player():
    global dealer_points
    global end_of_round
    card = deal_card(player_main_frame)
    player_hand.append(card)
    score = count_score(player_hand)
    player_score_value.set(score)
    if score > 21:
        if not end_of_round:
            result_value.set("Dealer wins")
            end_of_round = True
            dealer_points += 1
            dealer_pointing.set(dealer_points)


def play():
    main_window.mainloop()


main_window = tkinter.Tk()
main_window.geometry("680x400")
main_window.configure(background="green")

main_window["padx"] = 50
main_window.minsize(width=680, height=400)
main_window.maxsize(width=680, height=400)

main_window.columnconfigure(0, weight=1000)
main_window.columnconfigure(1, weight=1000)
main_window.columnconfigure(2, weight=1000)
main_window.columnconfigure(5, weight=1000)

result_value = create_top_frame()
dealer_main_frame, dealer_score_value, player_main_frame, player_score_value, cards_frame = create_card_frame()
create_button_frame()

cards = []
player_ace = False
load_cards(cards)

shuffled_cards = list(cards)
random.shuffle(shuffled_cards)

player_hand = []
dealer_hand = []
in_game_cards_frames = []

deal_player()
dealer_hand.append(deal_card(dealer_main_frame))
dealer_score_value.set(count_score(dealer_hand))
deal_player()

end_of_round = False
dealer_points = 0
player_points = 0
dealer_pointing, player_pointing = create_scoreboard()

if __name__ == "__main__":
    play()


