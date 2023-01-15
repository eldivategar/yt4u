from pytube import YouTube, Search
from flask import Flask, redirect, render_template, url_for, request, send_file, Response
import humanize

class MyApp():    

    def __init__(self):        
        self.app = Flask(__name__)        
        self.route() 
        self.link = None   
        self.judul = None        
        self.error = False

    def run(self):
        self.app.run()    
    
    def route(self):     

        @self.app.route('/', methods=['GET', 'POST'])
        def home():         
            if self.error == False:
                if request.method == 'POST' :
                    try:
                        self.link = request.form['link']
                        return redirect(url_for('getVideos'))
                    
                    except Exception as e:
                        return render_template('index.html', error = self.error)                                                              
                        
                return render_template('index.html')
            else:
                self.error = False
                return render_template('index.html', error = True)
            

        
        @self.app.route('/form-title')
        def home_title():
            return render_template('home-title.html')
        
        @self.app.route('/about')
        def about():
            return render_template('about.html')  

        @self.app.route('/pilih-resolusi')
        def getVideos():
            # self.link = request.form['link']            

            try:
                yt = YouTube(f'{self.link}')                
                judul = yt.title
                thumbnail = yt.thumbnail_url
                totalWaktu = yt.length
                totalViews = yt.views

                menit = totalWaktu // 60
                detik = totalWaktu % 60
                waktu = f'{menit}:{detik}'                                    

                # FILE MP4
                getFileMP4 = yt.streams.filter(type='video', progressive=True).desc()
                fileMP4 = {}
                fileMP4Final = {}
                for reso in getFileMP4:
                    resoi = reso.resolution
                    dt = yt.streams.filter(type='video', progressive=True, resolution=resoi).first()
                    filesize = dt.filesize    
                    fileMP4[resoi] = filesize 

                
                for i, v in fileMP4.items():
                    fileMP4Final[i] = humanize.naturalsize(v)


                # FILE MP3
                getFileMP3 = yt.streams.filter(only_audio=True).desc()
                fileMP3 = {}
                fileMP3Final = {}
                for abr in getFileMP3:
                    abri = abr.abr
                    dt = yt.streams.filter(only_audio=True, abr=abri).first()
                    filesize = dt.filesize
                    fileMP3[abri] = filesize
                
                for i, v in fileMP3.items():
                    fileMP3Final[i] = humanize.naturalsize(v) 
                    
                return render_template('resolution.html', link = self.link, judul = judul, thumbnail = thumbnail, fileMP4 = fileMP4Final, fileMP3 = sorted(fileMP3Final.items(), key=lambda x: int(x[0][:-4])), waktu = waktu)
                                                                               
            
            except Exception as e:
                self.error = True
                return redirect(url_for('home'))


        @self.app.route('/form-title', methods=['POST'])
        def searchTitle():
            if request.method == 'POST':
                try:
                    self.judul = request.form['judul']
                    getJudul = Search(str(self.judul))
                    result = getJudul.results[:15]                
                
                except Exception as e:
                    raise e

                return render_template('single-page-title.html', judul = self.judul, result = result)

        @self.app.route('/pilih-resolusi/https://youtube.com/watch?v=<video_id>')
        def getVideosByHref(video_id):
            self.link = (f'https://youtube.com/watch?v={video_id}')
            kilobyte = 1000
            megabyte = 1000000
            gigabyte = 1000000000
            
            try:
                yt = YouTube(f'{self.link}')                
                judul = yt.title
                thumbnail = yt.thumbnail_url
                totalWaktu = yt.length
                totalViews = yt.views           

                menit = totalWaktu // 60
                detik = totalWaktu % 60
                waktu = f'{menit}:{detik}'

               # FILE MP4
                getFileMP4 = yt.streams.filter(type='video', progressive=True).desc()
                fileMP4 = {}
                fileMP4Final = {}
                for reso in getFileMP4:
                    resoi = reso.resolution
                    dt = yt.streams.filter(type='video', progressive=True, resolution=resoi).first()
                    filesize = dt.filesize    
                    fileMP4[resoi] = filesize 

                
                for i, v in fileMP4.items():
                    fileMP4Final[i] = humanize.naturalsize(v)



                    # FILE MP3
                getFileMP3 = yt.streams.filter(only_audio=True).desc()
                fileMP3 = {}
                fileMP3Final = {}
                for abr in getFileMP3:
                    abri = abr.abr
                    dt = yt.streams.filter(only_audio=True, abr=abri).first()
                    filesize = dt.filesize
                    fileMP3[abri] = filesize

                    
                for i, v in fileMP3.items():
                    fileMP3Final[i] = humanize.naturalsize(v)                                
            
            except Exception as e:                
                raise e  
            
            return render_template('resolution.html', link = self.link, judul = judul, thumbnail = thumbnail, fileMP4 = fileMP4Final, fileMP3 = sorted(fileMP3Final.items(), key=lambda x: int(x[0][:-4])), waktu = waktu)   
        
        @self.app.route('/mp4<resolusi>')
        def get_mp4(resolusi):
            try:        
                yt = YouTube(self.link)                                
                judul = yt.title        

                dt = yt.streams.filter(resolution=resolusi, type='video', progressive=True).desc().first().download()              
                    
                return send_file(dt, as_attachment=True, attachment_filename=f'{judul} - ({resolusi}).mp4')
            
            except Exception as e :
                # raise e
                return render_template('resolusi.html', error = True)
            

        @self.app.route('/mp3<resolusi>')
        def get_mp3(resolusi): 
            try: 
                yt = YouTube(self.link)                  
                judul = yt.title

                dt = yt.streams.filter(only_audio=True, abr=str(resolusi)).first().download()

                return send_file(dt, as_attachment=True, attachment_filename=f'{judul} - ({resolusi}).mp3')      
            
            except Exception as e:
                # raise e
                return render_template('resolusi.html', error = True)
            
app = MyApp()
if __name__=='__main__':    
    app.run()