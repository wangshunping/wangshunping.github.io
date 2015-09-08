---
layout: post
title: 状态模式
description: ""
modified:
tags:
image:
    feature: abstract-6.jpg
category:
---

 **状态模式** 当一个对象的内在状态改变时允许改变其行为，这个对象看起来像是改变了其类。(DP)

当我们的代码中有这样的表达时，是不好的。

{% highlight python %}
def myFunc():
    if x > 90:
        print "a"
    elif x > 80:
        print "b"
    elif x > 70:
        print "c"
    elif x > 60:
        print "d"
    else:
        print "e"
{% endhighlight %}

因为 Long Method 可能是坏味道。

> 方法过长，且有很多的判断分支，就意味着它的责任过大了。无论是任何状态，都需要它改变，这实际上是很糟糕的。

上UML图

状态行为的好处就是，将与特定状态相关的行为局部化，并且将不同状态的行为分割开来。

将各种状态逻辑分割到子类之间，减少互相的依赖。

<figure><img src="/images/statue_pattern_UML.png" alt=""></figure>


py-pattern 项目里面关于状态模式的例子不可谓不经典。

{% highlight python %}
from __future__ import print_function

class State(object):

    """Base state. This is to share functionality"""

    def scan(self):
        """Scan the dial to the next station"""
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print("Scanning... Station is", self.stations[self.pos], self.name)


class AmState(State):

    def __init__(self, radio):
        self.radio = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos = 0
        self.name = "AM"

    def toggle_amfm(self):
        print("Switching to FM")
        self.radio.state = self.radio.fmstate


class FmState(State):

    def __init__(self, radio):
        self.radio = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos = 0
        self.name = "FM"

    def toggle_amfm(self):
        print("Switching to AM")
        self.radio.state = self.radio.amstate


class Radio(object):

    """A radio.     It has a scan button, and an AM/FM toggle switch."""

    def __init__(self):
        """We have an AM state and an FM state"""
        self.amstate = AmState(self)
        self.fmstate = FmState(self)
        self.state = self.amstate

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.state.scan()


# Test our radio out
if __name__ == '__main__':
    radio = Radio()
    actions = [radio.scan] * 2 + [radio.toggle_amfm] + [radio.scan] * 2
    actions *= 2

    for action in actions:
        action()

{% endhighlight %}

例子是这样的，有一个收音机，可以调到AM或者FM的状态。并且每个状态都有相同的方法，就是在特定频段间扫描。

不同的是，AM和FM扫描的频段是不同的。

于是有一个状态基类和他的两个子类AM和FM，他们都有的方法在基类中，不同的在子类中。

改变他们状态，就直接改变了实现。

以下是输出：

{% highlight python %}

### OUTPUT ###
# Scanning... Station is 1380 AM
# Scanning... Station is 1510 AM
# Switching to FM
# Scanning... Station is 89.1 FM
# Scanning... Station is 103.9 FM
# Scanning... Station is 81.3 FM
# Scanning... Station is 89.1 FM
# Switching to AM
# Scanning... Station is 1250 AM
# Scanning... Station is 1380 AM

{% endhighlight %}

这个例子棒极了。

于是我马上在我的代码中实现了一个。

需求是这样，前端有个选项，是判断是找所有的信息，或者是单个类别的信息。这两者的区别主要就在数据库查询语句的差别。

按照原来的实现，我至少有四个地方需要用到判断。于是我改成了状态模式。

上代码

{% highlight python %}
class State(mongoBase):


class totalState(State):

    def __init__(self, app):
        super(totalState, self).__init__()
        self.app = app

    def toggle_changeParent(self):
        self.app.state = self.app.specialState

    def run(self, start_time, end_time):

        #: for user info
        # for register
        pipeline = [
        ]

        # for order
        pipeline = [
        ]

        # get user register and common user from different platform

        #: Step 2: get order and deal info
        # get all new or common user

        for num, x in enumerate([newUserList, CommonUserList]):
            pipeline = [
            ]
            self.getOrder(pipeline, num)
            pipeline = [
            ]
            self.getDeal(pipeline, num)
        return returnStaff


class specialState(State):
    def __init__(self, app):
        self.app = app

class userMachine():
    """
        A Calc new/old user info Machine, it has an AllParent/SpecialParent switch.
    """
    def __init__(self,start_time, end_time):
        """
        we have an total state and specialParent state
        """
        self.totalstate = totalState(self)
        self.specialstate = specialState(self)
        self.state = self.totalstate
        self.start_time = start_time
        self.end_time = end_time

    def toggle_changeParent(self):
        self.state.toggle_changeParent()

    def run(self):
        self.state.run(self.start_time, self.end_time)

if __name__ == '__main__':
    start_time = '2015-08-22 00:00:00'
    end_time = '2015-08-23 00:00:00'
    app = userMachine(start_time, end_time)
    app.run()


{% endhighlight %}

只留下了代码骨架。

大量的mongo 聚合的pipeline都留到了子类里面，只要专注于定定不同的子类就可以了。即使下次做修改也十分便利。