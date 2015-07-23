# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2006 - 2007 Luis Carlos Dill Junges (lcdjunges@yahoo.com.br), Clovis Peruchi Scotti (scotti@ieee.org),
#                        Guilherme Augusto Rutzen (rutzen@das.ufsc.br), Mathias Erdtmann (erdtmann@gmail.com) and S2i (www.s2i.das.ufsc.br)
#            2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org), S2i (www.s2i.das.ufsc.br)
#
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License version 3, as published
#    by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranties of
#    MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#    PURPOSE.  See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    For further information, check the COPYING file distributed with this software.
#
#----------------------------------------------------------------------

from harpia.GladeWindow import GladeWindow
from harpia.amara import binderytools as bt
import gtk
from harpia.s2icommonproperties import S2iCommonProperties, APP, DIR
#i18n
import os
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

#----------------------------------------------------------------------
   
class Properties( GladeWindow, S2iCommonProperties ):

    #----------------------------------------------------------------------

    def __init__( self, PropertiesXML, S2iBlockProperties):
        
        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']
        
        filename = self.m_sDataDir+'glade/saveVideo.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'SAVEFilename',
            'SAVEType',
            'SAVEFrameRate',
            'BackgroundColor',
            'BorderColor',
            'codecSelection',
            'HelpView',
            'save_confirm'
            ]

        handlers = [
            'on_SAVEButtonSearch_clicked',
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_cancel_clicked',
            'on_save_confirm_clicked'
            ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)
        

        #load properties values
        for Property in self.m_oPropertiesXML.properties.block.property:

            if Property.name == "filename":
            	self.widgets['SAVEFilename'].set_text( os.path.expanduser(Property.value) );
            if Property.name == "framerate":
            	self.widgets['SAVEFrameRate'].set_value( float(Property.value) );
            if Property.name == "codecSelection":
            	if Property.value == "MPEG1":
            		self.widgets['codecSelection'].set_active(0)
            	elif Property.value == "mjpeg":
            		self.widgets['codecSelection'].set_active(1)
            	elif Property.value == "MPEG4.2":
            		self.widgets['codecSelection'].set_active(2)
            	elif Property.value == "MPEG4.3":
            		self.widgets['codecSelection'].set_active(3)
            	elif Property.value == "MPEG4":
            		self.widgets['codecSelection'].set_active(4)
            	elif Property.value == "H263":
            		self.widgets['codecSelection'].set_active(5)
            	elif Property.value == "H263I":
            		self.widgets['codecSelection'].set_active(6)
            	elif Property.value == "FLV1":
            		self.widgets['codecSelection'].set_active(7)

 #           if Property.name == "filetype":
 #               if Property.value == "png":
 #                   self.widgets['SAVEType'].set_active( int(0) )                    
 #               if Property.value == "jpeg":
 #                   self.widgets['SAVEType'].set_active( int(1) )


        self.configure()
                             
        #load help text
        t_oS2iHelp = bt.bind_file(self.m_sDataDir+"help/saveVideo"+ _("_en.help"))
        
        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text( unicode( str( t_oS2iHelp.help.content) ) )
    
        self.widgets['HelpView'].set_buffer( t_oTextBuffer )
        
    #----------------------------------------------------------------------

    def __del__(self):
        
	pass


    #----------------------------------------------------------------------
   
    def on_save_confirm_clicked( self, *args ):

        self.widgets['save_confirm'].grab_focus()

        for Property in self.m_oPropertiesXML.properties.block.property:
            
            if Property.name == "filename":
                Property.value = unicode( os.path.expanduser(self.widgets['SAVEFilename'].get_text()) )
            if Property.name == "framerate":
                Property.value = unicode( self.widgets['SAVEFrameRate'].get_value() )
            
            if Property.name == "codecSelection":
            	tCodec = int(self.widgets['codecSelection'].get_active())
            	if tCodec == 0:
            		Property.value = unicode("MPEG1")
            	elif tCodec == 1:
            		Property.value = unicode("mjpeg")
            	elif tCodec == 2:
            		Property.value = unicode("MPEG4.2")
            	elif tCodec == 3:
            		Property.value = unicode("MPEG4.3")
            	elif tCodec == 4:
            		Property.value = unicode("MPEG4")
            	elif tCodec == 5:
            		Property.value = unicode("H263")
            	elif tCodec == 6:
            		Property.value = unicode("H263I")
            	elif tCodec == 7:
            		Property.value = unicode("FLV1")

#            if Property.name == "filetype":
#
#               t_nActive = self.widgets['SAVEType'].get_active( )
#
#                if int(t_nActive) == 0:
#                    Property.value = unicode("png")
#                if int(t_nActive) == 1:
#                    Property.value = unicode("jpeg")

        self.m_oS2iBlockProperties.SetPropertiesXML( self.m_oPropertiesXML )

        self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )

        self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )
            
        self.widgets['Properties'].destroy()
            
    #----------------------------------------------------------------------

    def on_SAVEButtonSearch_clicked( self, *args ):

        dialog = gtk.FileChooserDialog("Salvar Video...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_SAVE, gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)

        if os.name == 'posix':
          dialog.set_current_folder(os.path.expanduser("~"))

        filter = gtk.FileFilter()
        filter.set_name("Todos os arquivos")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("videos")
        filter.add_mime_type("*.mpeg")
        filter.add_mime_type("*.avi")
        filter.add_mime_type("*.mpg")
        filter.add_mime_type("*.wmv")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            response =  dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            response = None
        dialog.destroy()

        self.widgets['SAVEFilename'].set_text(response);
        
    #----------------------------------------------------------------------
  
#SaveProperties = Properties()
#SaveProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
	global g_bSaveVideo
	g_bSaveVideo.append(blockTemplate.blockNumber)
	for propIter in blockTemplate.properties:
		if propIter[0] == 'filename':
			videoFilename = os.path.expanduser(propIter[1])
		if propIter[0] == 'framerate':
			frameRate = propIter[1]
		if propIter[0] == 'codecSelection':
			codecMacro = 'CV_FOURCC(\'P\',\'I\',\'M\',\'2\')'
			if propIter[1] == "MPEG1":
				codecMacro = 'CV_FOURCC(\'P\',\'I\',\'M\',\'2\')'
			if propIter[1] == "mjpeg":
				codecMacro = 'CV_FOURCC(\'M\',\'J\',\'P\',\'G\')'
			if propIter[1] == "MPEG4.2":
				codecMacro = 'CV_FOURCC(\'M\',\'P\',\'4\',\'2\')'
			if propIter[1] == "MPEG4.3":
				codecMacro = 'CV_FOURCC(\'D\',\'I\',\'V\',\'3\')'
			if propIter[1] == "MPEG4":
				codecMacro = 'CV_FOURCC(\'D\',\'I\',\'V\',\'X\')'
			if propIter[1] == "H263":
				codecMacro = 'CV_FOURCC(\'U\',\'2\',\'6\',\'3\')'
			if propIter[1] == "H263I":
				codecMacro = 'CV_FOURCC(\'I\',\'2\',\'6\',\'3\')'
			if propIter[1] == "FLV1":
				codecMacro = 'CV_FOURCC(\'F\',\'L\',\'V\',\'1\')'
	blockTemplate.imagesIO =  'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
									 'IplImage * block' + blockTemplate.blockNumber + '_img_o1 = NULL;\n' + \
									 'CvVideoWriter* block' + blockTemplate.blockNumber + '_vidWriter = NULL;\n'
	blockTemplate.functionCall = '\nif(block' + blockTemplate.blockNumber + '_img_i1){\n' +  \
											'	if(block' + blockTemplate.blockNumber + '_vidWriter == NULL)//video writer not started up yet!\n' + \
											'		block' + blockTemplate.blockNumber + '_vidWriter = cvCreateVideoWriter( "' + videoFilename + '", ' + codecMacro + ',' + frameRate + ', cvGetSize(block' + blockTemplate.blockNumber + '_img_i1), 1 );\n' + \
											'	cvWriteFrame( block' + blockTemplate.blockNumber + '_vidWriter, block' + blockTemplate.blockNumber + '_img_i1);\n' + \
											'	block' + blockTemplate.blockNumber + '_img_o1 = block' + blockTemplate.blockNumber + '_img_i1;\n' + \
											'}\n'
	blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n'

# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
	return {'Label':_('Save Video'),
         'Path':{'Python':'saveVideo',
                 'Glade':'glade/saveVideo.ui',
                 'Xml':'xml/saveVideo.xml'},
         'Inputs':1,
         'Outputs':1,
         'Icon':'images/saveVideo.png',
         'Color':'120:20:20:150',
				 'InTypes':{0:'HRP_IMAGE'},
				 'OutTypes':{0:'HRP_IMAGE'},
				 'Description':_('Save Video needs its description'),
				 'TreeGroup':_('General')
         }
