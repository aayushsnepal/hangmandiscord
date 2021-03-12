async def hangman(message):
    gameOver = False
    channel = message.channel
    user = message.author
    r = RandomWords()
    words = (str(r.get_random_word(maxLength=8))).lower()
    wo = words.lower()
    word = list(words)
    w = ""
    for x in word:
        w += x
    wordlength = len(word)
    await channel.send("Hangman started by " + user.mention)
    await channel.send("Word is " + str(wordlength) + " letters long!")

    attempts = 6

    correctguesses = []
    wrongguesses = []
    current = []
    for x in range(0, wordlength * 2 - 1):
        current.append(x)

    for x in range(0, wordlength * 2 - 1):
        if x % 2 == 0:
            current[x] = '_'
        else:
            current[x] = ' '

    st = "`"
    for e in current:
        st += e
    st += '`'
    await channel.send(st)
    while not gameOver and attempts > 0:
        await channel.send("Enter a letter: ")
        try:
            guess = await client.wait_for("message", timeout=10)
            if guess.author == message.author and len(guess.content.lower()) != 1 and guess.content.lower() != "quit" and \
                    guess.content.lower() != wo:
                await channel.send("One letter at a time.")
            else:
                if guess.author == message.author:
                    if guess.content == "quit":
                        await channel.send("Game exited. The word was `" + w + "`")
                        return
                    elif guess.content.lower() == wo:
                        gameOver = True
                        await channel.send("You guessed the word! The word was: `" + w + "`")
                    elif guess.content.lower() in word and guess.content.lower() not in correctguesses:
                        await channel.send("A correct letter!")
                        correctguesses.append(guess.content.lower())
                        x = 0
                        for i in word:
                            if i == guess.content.lower():
                                current[x * 2] = word[x]
                            x += 1
                    elif guess.content.lower() in correctguesses:
                        await channel.send("`" + guess.content.lower() + "` has already been guessed **correctly**!")
                    elif not gameOver:
                        if guess.content.lower() not in wrongguesses:
                            wrongguesses.append(guess.content.lower())
                            attempts -= 1
                            await channel.send("Wrong guess. Attempts left: " + str(attempts))
                        elif guess.content.lower() in wrongguesses:
                            await channel.send(
                                "`" + guess.content.lower() + "` has already been guessed **incorrectly**! Guess again.")
                    if not gameOver:
                        st = "`"
                        for e in current:
                            st += e
                        st += '`'
                        await channel.send(st)

                        if len(correctguesses) == 0:
                            s1 = ""
                        else:
                            s1 = "`"
                            for a in correctguesses:
                                s1 += a
                                s1 += ", "
                            s1 = s1[:-2]
                            s1 += '`'
                        await channel.send("Correct guesses: " + s1)
                        if len(wrongguesses) == 0:
                            s2 = ""
                        else:
                            s2 = "`"
                            for a in wrongguesses:
                                s2 += a
                                s2 += ", "
                            s2 = s2[:-2]
                            s2 += '`'
                            await channel.send("Wrong guesses: " + s2)

                if len(set(word)) == len(correctguesses):
                    gameOver = True
                    await channel.send("You won! The word was: `" + w + "`")
                if attempts == 0:
                    await channel.send("Out of attempts. The word was: `" + w + "`")
        except:
            await channel.send("Timed out! The word was: " + w)
            gameOver = True
