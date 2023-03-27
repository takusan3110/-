from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from mmpose.apis import (init_pose_model,  vis_pose_result, collect_multi_frames, process_mmdet_results, inference_top_down_pose_model)
from mmpose.datasets import DatasetInfo
from mmdet.apis import inference_detector, init_detector
import mmcv
import cv2
from sqlalchemy import create_engine , Column, Integer, Float, LargeBinary
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import os
import glob
import shutil
import datetime 
from os import urandom
import ffmpeg
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import re
import time

charset = "iso-2022-jp"

encoding='utf8'

app = Flask(__name__, static_folder='static')

#キーポイントリスト
k_list=[]
keypoints_list = [
     'nose',
     'left_eye',
     'right_eye',
     'left_ear',
     'right_ear',
     'left_shoulder',
     'right_shoulder',
     'left_elbow',
     'right_elbow',
     'left_wrist',
     'right_wrist',
     'left_hip',
     'right_hip',
     'left_knee',
     'right_knee',
     'left_ankle',
     'right_ankle']

##DB作成
database_file = os.path.join(os.path.abspath(os.getcwd()), 'data.db')
engine = create_engine('sqlite:///' + database_file, convert_unicode=True, echo=True)


#セッション(データベースとのやりとり)の設定
db_session = scoped_session( 
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = engine
    )
)
Base = declarative_base()
Base.query = db_session.query_property()

#必要な部分は変更する:主にpict～の数
# 画像データのカラム(列)の設定。画像の数に応じてクラスは増やす。
class SE(Base):
  __tablename__ = 'DataBase'
  id = Column(Integer, primary_key=True)
  date = Column(Float, unique=True)
  Original = Column(LargeBinary, unique=False)
  pict1 = Column(LargeBinary, unique=False)
  pict2 = Column(LargeBinary, unique=False)
  pict3 = Column(LargeBinary, unique=False) 

#各クラスをインスタンス化
  def __init__(self, Original=None, date=None, pict1=None, pict2=None, pict3=None):
    self.Original = Original
    self.date = date
    self.pict1 = pict1
    self.pict2 = pict2
    self.pict3 = pict3 

Base.metadata.create_all(bind=engine)




#検索機能:Testクラスを適した形、'Name'をテキストボックスの引数にして、==の先をdateにすれば名前一致で呼び出せるはず
#db = db_session.query(SE).filter(SE.'Name' == 1).all()


#秘密鍵生成
app.secret_key = urandom(24)

#ファイルアップロード(画像)
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # URLでhttp://127.0.0.1:5000/uploadを指定したときはGETリクエストとなるのでこっち
    if request.method == 'GET': 
        return render_template('InputPage_Image_PC.html')
    # 画像がアップロードされるとPOSTリクエストとなるのでこっち
    elif request.method == 'POST':
        start_time = time.time()
        file = request.files['uploadFile']
        file.save(os.path.join('./static/input_image', file.filename))
        #時刻表示の準備
        in_path = '/home/saitou/Documents/SE_mycode/static/input_image/'
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST) 
        #変更あり:主にクラス名と'Name'部分。クラスをカラムの設定で増やした場合はこちらにも追加する。
        d = now.strftime('%Y%m%d%H%M%S') # 現在時刻をYYYYMMDDhhmmss形式に書式化
        in_file_name = file.filename
        upload_file = d + '_' + in_file_name
        in_before = in_path + in_file_name
        in_after = in_path + upload_file
        os.rename(in_before, in_after)
    # 姿勢推定処理
    #フォルダから姿勢推定に使う画像を取り出す
        list_of_files = glob.glob('./static/input_image/*') 
        latest_file = max(list_of_files, key=os.path.getctime)
    #キーポイントのデータを読み込む(mmpose,mmdet)
        config_file = './static/mmpose/configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py'
        checkpoint_file = './static/pth/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth'
        det_config = './static/mmpose/demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py'
        det_checkpoint = './static/pth/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth'  
    #初期化処理
        pose_model = init_pose_model(config_file, checkpoint_file)
        det_model = init_detector(det_config, det_checkpoint)
    #推論検出    
        mmdet_results = inference_detector(det_model, latest_file)
    #検出結果から人物のバウンディングボックスを抽出 
        person_results = process_mmdet_results(mmdet_results, cat_id=1)
    #姿勢推定    
        pose_results,returned_outputs  = inference_top_down_pose_model(pose_model,
            latest_file,
            person_results,
            bbox_thr=0.3,
            format='xyxy',
            dataset=pose_model.cfg.data.test.type
           
            )

    #poseresultを可視化   
        vis_pose_result(pose_model, 
        latest_file, 
        pose_results, 
        dataset=pose_model.cfg.data.test.type, 
        out_file='vis_persons.jpeg')
        #出力ファイルを名前変えたり、移動させたり   
        shutil.move('./vis_persons.jpeg', './static/output_image')
        out_path = '/home/saitou/Documents/SE_mycode/static/output_image/'
        download_file = d + '_' + 'vis_persons.jpeg'
        out_before = out_path + 'vis_persons.jpeg'
        out_after = out_path + download_file
        os.rename(out_before, out_after)
        #pose_resultのキーポイントデータを.txt形式で保存
        with open("./static/output_keypoint_image/"+d+"_keypoints.txt", "w") as f:
            f.write(str(pose_results))
        #sessionに入れてoutputページに出力したい
        session['download_file'] = download_file
        session['out_after'] = out_after
        session['d']=d
        end_time = time.time()
        print("処理時間", end_time - start_time)
        #json_keypoints = json.dumps(pose_results)
        #session['json_keypoints']=json_keypoints
        return redirect(url_for('output'))

    #     pict = SE(Original= latest_file, date=d, pict1= vis_pose_result, pict2='Name', pict3='Name')#追加するデータの準備。各クラスに日付などで名前を付ける
    #  この二行で上で準備したデータを追加する
    #     db_session.add(pict)
    #     db_session.commit()
    #     db_session.close()
    #     return render_template('output_PC.html',  download_file=download_file)

#カメラからアップロード版
# @app.route('/camera', methods=['GET','POST'])
# def camera():
#     # if request.method == 'GET': 
#     #     return render_template('camera_PC.html')

#     # elif request.method == 'POST':
#     #     file = request.form['img']
#     #     file.save(os.path.join('./static/input_movie', file.filename)) 
#     # # 姿勢推定処理
#     #     list_of_files = glob.glob('./static/input_movie/*') 
#     #     latest_file = max(list_of_files, key=os.path.getctime)
#     #     config_file = 'associative_embedding_hrnet_w32_coco_512x512.py'
#     #     checkpoint_file = 'hrnet_w32_coco_512x512-bcb8c247_20200816.pth'
#     #     pose_model = init_pose_model(config_file, checkpoint_file, device='cpu')  
#     #     pose_results, _ = inference_bottom_up_pose_model(pose_model, latest_file)
#     #     vis_pose_result(pose_model, latest_file, pose_results, out_file='vis_persons.mp4')
#     #     shutil.move('./vis_persons.mp4', './static/input_movie')
#     #     pose_results_path = "./static/input_movie/vis_persons.jpg"

#ファイルアップロード（動画）
@app.route("/upload_movie", methods=['GET', 'POST'])
def upload_movie():
        # URLでhttp://127.0.0.1:5000/uploadを指定したときはGETリクエストとなるのでこっち
    if request.method == 'GET': 
        return render_template('InputPage_Movie_PC.html')
    # 動画がアップロードされるとPOSTリクエストとなるのでこっち
    elif request.method == 'POST':
            file = request.files['uploadFile_movie']
            file.save(os.path.join('./static/input_movie', file.filename))
        #時刻表示の準備
            in_path = '/home/saitou/Documents/SE_mycode/static/input_movie/'
            t_delta = datetime.timedelta(hours=9)
            JST = datetime.timezone(t_delta, 'JST')
            now = datetime.datetime.now(JST) 
        
        #現在時刻の取得とファイル名変更
            d = now.strftime('%Y%m%d%H%M%S') 
            in_file_name = file.filename
            upload_file = d + '_' + in_file_name
            in_before = in_path + in_file_name
            in_after = in_path + upload_file
            os.rename(in_before, in_after)
        
        # 姿勢推定処理
            list_of_files = glob.glob('./static/input_movie/*') 
            latest_file = max(list_of_files, key=os.path.getctime)
            video = mmcv.VideoReader(latest_file) 

        #video保存
            fps = video.fps
            size = (video.width, video.height)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            videoWriter = cv2.VideoWriter(
            os.path.join('./static/output_movie',
                         f'vis_{os.path.basename(latest_file)}'), fourcc,
                    fps, size)
 
        #mmpose用データ    
            config_file = './static/mmpose/configs/body/2d_kpt_sview_rgb_vid/posewarper/posetrack18/hrnet_w48_posetrack18_384x288_posewarper_stage2.py'
            checkpoint_file = './static/pth/hrnet_w48_posetrack18_384x288_posewarper_stage2-4abf88db_20211130.pth'
        #mmdet用データ    
            det_config = './static/mmpose/demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py'
            det_checkpoint = './static/pth/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth'  
        #初期化処理
            pose_model = init_pose_model(config_file, checkpoint_file)
            det_model = init_detector(det_config, det_checkpoint)
        #下準備
            indices = pose_model.cfg.data.test.data_cfg['frame_indices_test']
        #dataset用データ
            dataset = pose_model.cfg.data['test']['type']
            dataset_info = pose_model.cfg.data['test'].get('dataset_info', None)
            dataset_info = DatasetInfo(dataset_info)   
        #推論検出 
            for frame_id, cur_frame in enumerate(mmcv.track_iter_progress(video)):
                mmdet_results = inference_detector(det_model, cur_frame)
        #検出結果から人物のバウンディングボックスを抽出 
                person_results = process_mmdet_results(mmdet_results, cat_id=1)
                frames = collect_multi_frames(video, frame_id, indices, online=True)        
                pose_results, returned_outputs = inference_top_down_pose_model(
                    pose_model,
                    frames,
                    person_results,
                    bbox_thr=0.3,
                    format='xyxy',
                    dataset=dataset,
                    dataset_info=dataset_info,
                    return_heatmap=False,
                    outputs=None)
                vis_frame = vis_pose_result(
                    pose_model,
                    cur_frame,
                    pose_results,
                    dataset=dataset_info, 
                    kpt_score_thr=0.3,
                    radius=4,
                    thickness=1,
                    show=False)
                videoWriter.write(vis_frame)
            videoWriter.release()
            list_of_movies_out = glob.glob('./static/output_movie/*') 
            latest_movie_out = max(list_of_movies_out, key=os.path.getctime)
            (
                ffmpeg
                .input(latest_movie_out)
                .output("./static/output_movie/decode" +d+".mp4", vcodec='libx264')
                .run()
            )
        #pose_resultのキーポイントデータを.txt形式で保存
            with open("./static/output_keypoint_movie/"+d+"_keypoints.txt", "w") as f:
                f.write(str(pose_results))
        #メール送信
            To = request.form.get('email')
            if To:
                Subject = "姿勢推定結果のお知らせ"
                #MailBody = "http://127.0.0.1:5000/" + str(f'vis_{os.path.basename(latest_file)}')
                MailBody = """下記URLにアクセスし、IDを入力してください。
                                http://157.16.107.196:5000//email_form
                                ID: decode"""+d+""".mp4"""
        #SMTPサーバー接続・ログイン情報
                my_mail = "shiseidou06@gmail.com"
                app_password = "kfukyljgserdboow"
                smtp = smtplib.SMTP("smtp.gmail.com",587)

                From = my_mail
                Atesaki = To
                Kenmei = Subject
                Body = MailBody
                
                #メール本文を読込
                #msg = MIMEText(Body,"plain",charset)
                msg = MIMEMultipart()
                msg.attach(MIMEText(Body))
                msg["Subject"] = Header(Kenmei.encode(charset),charset)

                """ メールサーバー接続（編集不要）"""
                #サーバー・ポート接続
                smtp.ehlo()
                #TLS暗号化
                smtp.starttls()
                #SMTPサーバーログイン
                smtp.login(my_mail,app_password)
                #メール送信
                smtp.sendmail(From,Atesaki,msg.as_string())
                #SMTPサーバー遮断
                smtp.quit()

                return """メールの送信が完了しました"""
            session['d']=d
            session['latest_movie_out']=latest_movie_out
            return redirect(url_for('output_movie'))
            
                
            
            
        

#topページをクリック 
@app.route("/", methods=["GET"])
def top():
    return render_template("TopPage_PC.html")

#aboutページをクリック 
@app.route("/about", methods=["GET"])
def about():
    return render_template("about_PC.html")

#useページをクリック 
@app.route("/use", methods=["GET"])
def use():
    return render_template("use_PC.html")

#infoページをクリック 
@app.route("/info", methods=["GET"])
def info():
    return render_template("info_PC.html")

#contactページをクリック 
@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact_PC.html")

#termsページをクリック
@app.route("/terms", methods=["GET"])
def terms():
    return render_template("terms_PC.html")

#loadingページ
@app.route("/loading", methods=["GET"])
def loading():
    return render_template("loading.html")

#outputページをクリック
@app.route("/output", methods=['GET', 'POST'])
def output():
    download_file = session.get('download_file')
    out_after = session.get('out_after')
    d=session.get('d')
    #json_pose_results = json.dumps(pose_results)
    #json_keypoints=session.get('json_keypoints')
    if request.method == 'POST':
        return render_template("output_PC.html", download_file=download_file,out_after=out_after,d=d)
        #return render_template("output_PC.html", download_file=download_file,out_after=out_after, json_keypoints=json_keypoints)
    elif request.method == 'GET':
        return render_template("output_PC.html", download_file=download_file,out_after=out_after, d=d)
        #return render_template("output_PC.html", download_file=download_file, out_after=out_after, json_keypoints=json_keypoints)

@app.route("/output_movie", methods=['GET', 'POST'])
def output_movie():
    d=session.get('d')
    latest_movie_out=session.get('latest_movie_out')
    if request.method == 'POST':
        return render_template("output_movie_PC.html", latest_movie_out=latest_movie_out, d=d)
    elif request.method == 'GET':
        return render_template("output_movie_PC.html", latest_movie_out=latest_movie_out, d=d)

#メール送信用ページ
@app.route("/email_form", methods=['GET', 'POST'])
def email_form():
    return render_template("email_form.html")

#outputページ(メール利用時)
@app.route("/email_output", methods=['GET', 'POST'])
def email_output():
    id = request.form['id']
    if id.endswith('.mp4'):
        path = "./static/output_movie/" + id
        match = re.search(r"decode(\d{14})", id)
        d = match.group(1)
        return render_template("email_output.html", id=id, d=d, path=path)
    else:
        return redirect(url_for('email_form'))

##動画再生用

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')



