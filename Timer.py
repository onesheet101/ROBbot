from discord.ext import tasks


class Timer:

    def __init__(self, coginstance, member):
        self.member = member
        self.coginstance = coginstance
        self.timer.start()

    # This loop is called when the Timer object is initialised.
    # Waits 5 minutes.
    @tasks.loop(minutes=5, count=1)
    async def timer(self):
        pass

    # Decorator means this function is called after the loop has ended.
    # Simply calls the end of timer function associated with main instance of the Quiz object.
    @timer.after_loop
    async def ended(self):
        await self.coginstance.end_of_timer(self.member)
