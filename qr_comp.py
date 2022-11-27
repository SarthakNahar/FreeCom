import cv2
import pyzbar.pyzbar as pyzbar
#import webbrowser
def dummy_file(qpro):
    print(qpro)
    file=open('dummy.txt','w')
    file.writelines(qpro)
    file.close()

def generate_frames_qrComp():
    cap=cv2.VideoCapture(0)
    cap.set(3,1000)  # Webcam Width & Height
    cap.set(4,600)
    detector = cv2.QRCodeDetector()
    seen = set()
    uniq = []
    while True:
            
        ## read the camera frame
        success,frame=cap.read()
        decodedObjects = pyzbar.decode(frame) # Decoding qr code data

        cv2.rectangle(frame,(0,0),(1000,80),(245,176,66),-1) # Background rectangle to display text

        for obj in decodedObjects : 

            data = obj.data.decode('utf-8')
            x=str(data) # data in string
            if x not in seen: # taking only unique qr code 
                uniq.append(x+'\n')
                seen.add(x)

            cv2.putText(frame,data,(20,50),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,250),2) # Display data in qr code

            x,y,w,h = obj.rect # get qr code coordinates to draw rectangle
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,250,0),2) # Rectangle around qr code
            print(data)
    
            try:
                if len(seen)==2:
                    print("OK list is: ",uniq)
                    cap.release()
                    cv2.destroyAllWindows()
                    dummy_file(uniq)
            except:
                pass
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def __del__(self):
        try: 
            self.cap.stop()
            self.cap.stream.release()
        except:
            print('probably there\'s no cap yet :(')
        cv2.destroyAllWindows()