import Board as Bd
import time
import array
import threading
import numpy

def DataThread(Session):


    Session.myBoard.run()
    time.sleep(0.01)
    status, curr_index, curr_count = Session.myBoard.getStatus()

    if Session.RespON:
        time.sleep(0.4)
        Session.myBoard.ConfigDigitalPort()
        TestEpoch = int(Session.myBoard.SRate // 10)
        MinTime = time.time()
    else:
        time.sleep(0.01)

    ini = curr_index

    if Session.isRecording:
        Session.Date = Session.GetDateStr()
        RawDataFile = open(Session.FileName + Session.Date + ".dat", 'w+b')
        if Session.RespON:
            RespFile = open(Session.FileName + Session.Date + ".resp", 'w+b')
        Session.SaveSessionSettings()

    Session.DisplaySettings()

    while Session.isAcquiring == True:

        # Make sure a data point is available for display.
        time.sleep(0.01)
        status, curr_index, curr_count = Session.myBoard.getStatus()


        if curr_index != ini:

            if curr_index < ini:
                d_array = array.array('d', Session.myBoard.PtrMemhandle[ini:Session.myBoard.total_count]
                                      + Session.myBoard.PtrMemhandle[0:curr_index])

            else:
                d_array = array.array('d', Session.myBoard.PtrMemhandle[ini:curr_index])

            ini = curr_index
            if Session.isRecording:
                d_array.tofile(RawDataFile)

            for ch in range(Session.myBoard.Channels):

                ts = d_array[ch::Session.myBoard.Channels]

                if Session.RespON and Session.RespCh == ch:

                    #Respiration stuff
                    Session.RespBuffer = Session.RespBuffer[ts.__len__():] + ts

                    RespMean = numpy.mean(Session.RespBuffer)
                    RespThresh= RespMean - numpy.std(Session.RespBuffer)

                    if time.time() - MinTime > 0.1 and \
                            any(Session.RespBuffer[-TestEpoch:-1] < RespThresh) and \
                            Session.RespBuffer[-1] > RespMean:

                        Session.myBoard.TTLSwitch()
                        Session.Canvases[ch].plotResp(ts,min(Session.RespBuffer), max(Session.RespBuffer))
                        MinTime = time.time()
                        if Session.isRecording:
                            array.array('I', [curr_count]).tofile(RespFile)

                    else:
                        Session.Canvases[ch].plot(ts)

                else:
                    Session.Canvases[ch].plot(ts)

    if Session.isRecording:
        RawDataFile.close()
        if Session.RespON:
            RespFile.close()
    Session.myBoard.stop()


class Session():

    VisWindowLength = 0
    Canvases = []
    isAcquiring = False
    isRecording = False
    FileName = ""
    Date = ""

    RespON = False
    RespCh = 0
    RespBuffer = 0

    #Board params
    BoardCreated = False
    Descriptor = 0
    BoardNum = 0
    VRange = 0
    SRate = 0
    Channels = 0
    BoardStr = ""

    def createBoard(self):

        self.myBoard = Bd.Board(self.Descriptor,self.BoardNum,self.VRange,self.SRate,self.Channels)
        self.BoardCreated = True

    def AcquireData(self):

        self.isAcquiring = True

        if self.RespON:
            self.RespBuffer = array.array('d',[0] * self.myBoard.SRate)


        self.t1 = threading.Thread(target=DataThread, args=(self,))
        self.t1.start()


    def StopAcquisition(self):

        self.isAcquiring = False
        self.t1.join()

    def GetDateStr(self):

        Date = "_" + str(time.localtime().tm_mon) + "_" \
               + str(time.localtime().tm_mday) + "_" \
               + str(time.localtime().tm_year) + "_" \
               + str(time.localtime().tm_hour) + "_" \
               + str(time.localtime().tm_min) + "_" \
               + str(time.localtime().tm_sec)

        return Date

    def SaveSessionSettings(self):

        SessionSettingsFile = open("SessionSettings_" +  self.FileName +self.Date + ".txt", 'w')

        SessionSettingsFile.write("filename=" + self.FileName + ",\n")
        SessionSettingsFile.write("rate=" + str(self.SRate) + ",\n")
        SessionSettingsFile.write("range=±" + str(self.VRange) + ",\n")
        SessionSettingsFile.write("channels=" + str(self.Channels) + ",\n")

        if self.RespON:
            SessionSettingsFile.write("RespON=True" + ",\n")
            SessionSettingsFile.write("RespChan=" + str(self.RespCh) + ",\n")
        else:
            SessionSettingsFile.write("RespON=False" + ",\n")

        SessionSettingsFile.write("board=" + self.BoardStr + ",\n")

        SessionSettingsFile.close()

    def DisplaySettings(self):

        if self.isRecording:
            print("Recording=True")
            print("filename=" + self.FileName + self.Date)
        else:
            print("Recording=False")


        print("rate=" + str(self.SRate) + "Hz")
        print("range=±" + str(self.VRange) + "V")
        print("channels=" + str(self.Channels))
        if self.RespON:
            print("RespON=True")
            print("RespChan=" + str(self.RespCh))
        else:
            print("RespON=False")

    def EndSession(self):

        if self.isAcquiring:
            self.StopAcquisition()

        if self.BoardCreated:
            self.myBoard.ReleaseBoard()