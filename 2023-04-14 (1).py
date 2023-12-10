import flask,json,os
from linebot import LineBotApi
import linebot.models as bm
import openai
import speech_recognition as sp
p1=sp.Recognizer()
openai.api_key=""
bot=LineBotApi("")
f=flask.Flask("testbot")
@f.route("/",methods=["GET","POST"])
def home():
	data=flask.request.get_data(as_text=True)
	d=json.loads(data)
	print("使用者ID：",d["events"][0]["source"]["userId"])
	print("狀態：",d["events"][0]["type"])
	if d["events"][0]["type"]=="message":
		print("回覆Token：",d["events"][0]["replyToken"])
		print("訊息類型：",d["events"][0]["message"]["type"])
		if d["events"][0]["message"]["type"]=="text":
			print("訊息內容：",d["events"][0]["message"]["text"])
			rep=openai.ChatCompletion.create(
				model="gpt-3.5-turbo" ,
				messages=[
					{"role":"user","content":"請使用繁體中文"},
					{"role":"user","content":d["events"][0]["message"]["text"]}
				] ,
				temperature=0.5,
				max_tokens=4000
			)
			bot.push_message(
				d["events"][0]["source"]["userId"] ,
				bm.TextSendMessage(text=rep.choices[0].message.content)
			)
			# bot.push_message(
			# 	d["events"][0]["source"]["userId"] ,
			# 	bm.StickerSendMessage(
			# 		package_id="789",
			# 		sticker_id="10855"
			# 	)
			# )
			# bot.push_message(
			# 	d["events"][0]["source"]["userId"] ,
			# 	bm.ImageSendMessage(
			# 		original_content_url="https://eabf-114-44-128-250.ngrok-free.app/image.jpg" ,
			# 		preview_image_url="https://eabf-114-44-128-250.ngrok-free.app/preview.jpg"
			# 	)
			# )
			# bot.push_message(
			# 	d["events"][0]["source"]["userId"] ,
			# 	bm.LocationSendMessage(
			# 		title="創客基地" ,
			# 		address="台北市大安區" ,
			# 		latitude=20 ,
			# 		longitude=30
			# 	)
			# )
		elif d["events"][0]["message"]["type"]=="sticker":
			print("貼圖群組：",d["events"][0]["message"]["packageId"])
			print("貼圖編號：",d["events"][0]["message"]["stickerId"])
		elif d["events"][0]["message"]["type"]=="location":
			print("緯度：",d["events"][0]["message"]["latitude"])
			print("經度：",d["events"][0]["message"]["longitude"])
			print("地址：",d["events"][0]["message"]["address"])
			if "title" in d["events"][0]["message"]:
				print("名稱：",d["events"][0]["message"]["title"])
		else:
			fileID=d["events"][0]["message"]["id"]
			print("檔案ID：",fileID)
			if d["events"][0]["message"]["type"]=="image":
				fileName=fileID+".png"
			elif d["events"][0]["message"]["type"]=="video":
				fileName=fileID+".mp4"
			elif d["events"][0]["message"]["type"]=="audio":
				fileName=fileID+".m4a"
			file=bot.get_message_content(fileID)
			with open("file/"+fileName, "wb") as fs:
				fs.write(file.content)
			if d["events"][0]["message"]["type"]=="audio":
				os.system(f"ffmpeg -y -i file/{fileName} file/{fileID}.aiff")
				with sp.AudioFile("file/"+fileID+".aiff") as src:
					sound=p1.record(src)
					text=p1.recognize_google(sound, language="zh-TW")
					bot.push_message(
						d["events"][0]["source"]["userId"] ,
						bm.TextSendMessage(text=text)
					)
	return "TEST..."
@f.route("/<string:fn>", methods=["GET"])
def test(fn):
	return flask.send_from_directory(
		"./" ,
		fn ,
		as_attachment=False
	)
f.run(port=80)
