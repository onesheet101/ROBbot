from discord.ext import tasks


class Timer:

    def __init__(self, coginstance, member):
        self.coginstance = coginstance
        self.member = member
        self.timer.start()

    @tasks.loop(minutes=5, count=1)
    async def timer(self):
        pass

    @timer.after_loop
    async def ended(self):
        await self.coginstance.end_of_timer(self.member)
