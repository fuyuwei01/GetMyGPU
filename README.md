# GetMyGPU——用于多卡环境自动运行训练的脚本
实验室的GPU经常被抢，很难过，所以写了这个脚本。

设置好参数后，直接

```
python getGPU.py
```

即可。

仅适用于在Linux环境中进行深度学习训练的场景。



### server酱

支持server酱使用，当训练开始时会推送一条消息至你的微信。

你可以在sct.ftqq.com中获取你的专属sendkey，并在本脚本中设置好相应参数即可使用。