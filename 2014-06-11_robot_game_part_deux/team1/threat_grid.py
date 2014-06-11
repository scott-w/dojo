import rg


class Robot:
    """
    """
    def act(self, game):
        """
        """

        locations = []
        for loc in rg.locs_around(self.location, filter_out=('invalid', 'obstacle')):
            danger = self._get_danger(game, loc)
            locations.append((loc, danger))

        locations = sorted(locations, lambda x, y: x[1] - y[1])

        attack = None
        for loc in locations:
            enemies = self._get_enemies(game, loc)
            if loc[0] in [e[0] for e in enemies]:
                attack = loc[0]
                break

        if attack is None:
            return ['move', locations[0][0]]
        return ['attack', attack]

    def _get_danger(self, game, loc):
        """Returns the danger of the given location as an integer between
        1 and 10.
        """
        baseline = 5
        if 'spawn' in rg.loc_types(loc):
            baseline += 2
        
        enemy_bots = self._get_enemies(game, loc)
        for enemy_loc, bot in enemy_bots:
            if enemy_loc in rg.locs_around(loc):
                baseline = 10 # Can't go here

            for adj in rg.locs_around(loc):
                if adj in rg.locs_around(enemy_loc):
                    baseline += (bot.hp - self.hp) // 10

        friends = self._get_friends(game, loc)
        for friend_loc, bot in friends:
            if friend_loc in rg.locs_around(loc):
                baseline = 10 # Can't go here

        if baseline < 1:
            baseline = 1
        elif baseline > 10:
            baseline = 10

        return baseline

    def _get_enemies(self, game, loc):
        enemy_bots = [
            (loc, bot)
            for loc, bot in game.robots.iteritems()
            if bot.player_id != self.player_id
            and rg.wdist(loc, self.location) < 3]

        return enemy_bots

    def _get_friends(self, game, loc):
        return [
            (loc, bot)
            for loc, bot in game.robots.iteritems()
            if bot.player_id == self.player_id
            and rg.wdist(loc, self.location) < 3]
