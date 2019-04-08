receive from wechat：
1.event 事件
1.1subscribe 粉丝关注
<xml>
    <ToUserName><![CDATA[gh_9ccb884dca41]]></ToUserName>\n
    <FromUserName><![CDATA[o466w0-wxxlA7oDpnuL4F8aNOtrY]]></FromUserName>\n
    <CreateTime>1549935250</CreateTime>\n
    <MsgType><![CDATA[event]]></MsgType>\n
    <Event><![CDATA[subscribe]]></Event>\n
    <EventKey><![CDATA[]]></EventKey>\n
</xml>
1.2unsubscribe 粉丝取消关注
<xml>
    <ToUserName><![CDATA[gh_9ccb884dca41]]></ToUserName>\n
    <FromUserName><![CDATA[o466w0-wxxlA7oDpnuL4F8aNOtrY]]></FromUserName>\n
    <CreateTime>1549935223</CreateTime>\n
    <MsgType><![CDATA[event]]></MsgType>\n
    <Event><![CDATA[unsubscribe]]></Event>\n
    <EventKey><![CDATA[]]></EventKey>\n
</xml>
1.3MASSSENDJOBFINISH 群发消息推送结果
<xml>
    <ToUserName><![CDATA[gh_9ccb884dca41]]></ToUserName>\n
    <FromUserName><![CDATA[o466w08KPIETfyjRhVJe2utMdNXE]]></FromUserName>\n
    <CreateTime>1550021206</CreateTime>\n
    <MsgType><![CDATA[event]]></MsgType>\n
    <Event><![CDATA[MASSSENDJOBFINISH]]></Event>\n
    <MsgID>1000000016</MsgID>\n
    <Status><![CDATA[send success]]></Status>\n
    <TotalCount>22</TotalCount>\n
    <FilterCount>22</FilterCount>\n
    <SentCount>22</SentCount>\n
    <ErrorCount>0</ErrorCount>\n
    <CopyrightCheckResult>
        <Count>0</Count>\n
        <ResultList></ResultList>\n
        <CheckState>0</CheckState>\n
    </CopyrightCheckResult>\n
</xml> 

2.chat 聊天
2.1text
<xml>
    <ToUserName><![CDATA[gh_9ccb884dca41]]></ToUserName>\n
    <FromUserName><![CDATA[o466w0-wxxlA7oDpnuL4F8aNOtrY]]></FromUserName>\n
    <CreateTime>1549074674</CreateTime>\n
    <MsgType><![CDATA[text]]></MsgType>\n
    <Content><![CDATA[你好]]></Content>\n
    <MsgId>22177419451303285</MsgId>\n
</xml>

2.2image
<xml>
    <ToUserName><![CDATA[gh_9ccb884dca41]]></ToUserName>\n
    <FromUserName><![CDATA[o466w0-wxxlA7oDpnuL4F8aNOtrY]]></FromUserName>\n
    <CreateTime>1549074760</CreateTime>\n
    <MsgType><![CDATA[image]]></MsgType>\n
    <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/7Sz0BKveCVkNOm0Wpfbsq6eJfNK1RT3vLCAqmttkkuxrIrTlEKnPSRLhwIL4QuicdLvRQDUHvwNpMhsUNY3YicuQ/0]]></PicUrl>\n
    <MsgId>22177419790819336</MsgId>\n
    <MediaId><![CDATA[pS4KZV82SfpTvvMU65HIszubfwFFWQJQHnIxB0i0a7hWAcafFH3uzaxKvU3CFsfc]]></MediaId>\n
</xml>

2.3voice
<xml>
    <ToUserName><![CDATA[gh_9ccb884dca41]]></ToUserName>\n
    <FromUserName><![CDATA[o466w0-wxxlA7oDpnuL4F8aNOtrY]]></FromUserName>\n
    <CreateTime>1549074861</CreateTime>\n
    <MsgType><![CDATA[voice]]></MsgType>\n
    <MediaId><![CDATA[SvByueEwJmJGj4AgZGE3aZWJNK9YS4-eoN1CezVEU_9mgyfscpd-W1cqTRcxdZ0n]]></MediaId>\n
    <Format><![CDATA[amr]]></Format>\n
    <MsgId>22177419830367883</MsgId>\n
    <Recognition><![CDATA[]]></Recognition>\n
</xml>

2.4video
<xml>
    <ToUserName><![CDATA[gh_9ccb884dca41]]></ToUserName>\n
    <FromUserName><![CDATA[o466w0-wxxlA7oDpnuL4F8aNOtrY]]></FromUserName>\n
    <CreateTime>1549074979</CreateTime>\n
    <MsgType><![CDATA[video]]></MsgType>\n
    <MediaId><![CDATA[XMWlMGPis5YpxJb3VKDANSdcE2gi0P9UATW8SSDMU_5dDwjXIOfcl6E4p2SnHRJP]]></MediaId>\n
    <ThumbMediaId><![CDATA[FZUFznvgufQ2oKlqzBCuOkMAQIV7rq3Wwd7amn9QHcWcRGOP7IzJ8Zi-vmXl1-LH]]></ThumbMediaId>\n
    <MsgId>22177423625142691</MsgId>\n
</xml>

2.5shotvideo

2.6location
<xml>
    <ToUserName><![CDATA[gh_9ccb884dca41]]></ToUserName>\n
    <FromUserName><![CDATA[o466w0-wxxlA7oDpnuL4F8aNOtrY]]></FromUserName>\n
    <CreateTime>1549075172</CreateTime>\n
    <MsgType><![CDATA[location]]></MsgType>\n
    <Location_X>31.190313</Location_X>\n
    <Location_Y>121.606636</Location_Y>\n
    <Scale>16</Scale>\n
    <Label><![CDATA[银联商务(浦东新区张衡路1006号)]]></Label>\n
    <MsgId>22177424036326378</MsgId>\n
</xml>

2.7link
<xml>
    <ToUserName><![CDATA[gh_9ccb884dca41]]></ToUserName>\n
    <FromUserName><![CDATA[o466w0-wxxlA7oDpnuL4F8aNOtrY]]></FromUserName>\n
    <CreateTime>1549069924</CreateTime>\n
    <MsgType><![CDATA[link]]></MsgType>\n
    <Title><![CDATA[“三次握手，四次挥手”你真的懂吗？]]></Title>\n
    <Description><![CDATA[作为程序员，要有“刨根问底”的精神。知其然，更要知其所以然。这篇文章希望能抽丝剥茧，还原背后的原理。]]></Description>\n
    <Url><![CDATA[http://mp.weixin.qq.com/s?__biz=MzAxODI5ODMwOA==&mid=2666543559&idx=1&sn=83cf0e9367511d6b311909a5b3dfc81e&chksm=80dcfd6cb7ab747af19259cce70621b269c5fae25582af7c57f5be904bc18e216625cf6f4157&mpshare=1&scene=24&srcid=01124lOxAPNk0eS7V1REpEGP#rd]]></Url>\n
    <MsgId>22177350887961026</MsgId>\n
</xml>