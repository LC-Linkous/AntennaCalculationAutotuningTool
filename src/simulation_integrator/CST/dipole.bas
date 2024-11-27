' dipole
' !!! Do not change the line above !!!


Option Explicit 

Sub Main ()
Dim studio As Object
Set studio = CreateObject("CSTStudio.Application") ''"MWStudio.Application"

Dim mws As Object
Set mws = studio.NewMWS


BeginHide
	StoreDoubleParameter "r", 1
	SetParameterDescription  ( "r",  "wire radius"  )
	StoreDoubleParameter "gap", 5
	SetParameterDescription  ( "gap",  "strip distance"  )
	StoreDoubleParameter "N", 5
	SetParameterDescription  ( "N",  "strip length in multiples of N*gap"  )
	StoreDoubleParameter "L", 80
	SetParameterDescription  ( "L",  "Dipole-Length/2"  )
EndHide


'@ new component: component1
Component.New "component1" 


'@ define cylinder: component1:wire1
With Cylinder 
     .Reset 
     .Name "wire1" 
     .Component "component1" 
     .Material "PEC" 
     .OuterRadius "r" 
     .InnerRadius "0" 
     .Axis "z" 
     .Zrange "0", "L" 
     .Xcenter "0" 
     .Ycenter "0" 
     .Segments "0" 
     .Create 
End With 


'@ transform: translate component1:wire1
With Transform 
     .Reset 
     .Name "component1:wire1" 
     .Vector "0", "0", "gap/2" 
     .UsePickedPoints "False" 
     .InvertPickedPoints "False" 
     .MultipleObjects "False" 
     .GroupObjects "False" 
     .Repetitions "1" 
     .MultipleSelection "False" 
     .TranslateAdvanced 
End With 


'@ transform: mirror component1:wire1
With Transform 
     .Reset 
     .Name "component1:wire1" 
     .Origin "Free" 
     .Center "0", "0", "0" 
     .PlaneNormal "0", "0", "1" 
     .MultipleObjects "True" 
     .GroupObjects "False" 
     .Repetitions "1" 
     .MultipleSelection "False" 
     .Component "" 
     .Material "" 
     .MirrorAdvanced 
End With 


'@ pick face
Pick.PickFaceFromId "component1:wire1_1", "1" 


'@ align wcs with face
WCS.AlignWCSWithSelectedFace 
Pick.PickCenterpointFromId "component1:wire1_1", "1" 
WCS.AlignWCSWithSelectedPoint 


'@ define brick: component1:strip1
With Brick
     .Reset 
     .Name "strip1" 
     .Component "component1" 
     .Material "PEC" 
     .Xrange "-2*r", "N*gap" 
     .Yrange "-2*r", "2*r" 
     .Zrange "0", "gap/10" 
     .Create
End With


'@ activate global coordinates
WCS.ActivateWCS "global"


'@ transform: mirror component1:strip1
With Transform 
     .Reset 
     .Name "component1:strip1" 
     .Origin "Free" 
     .Center "0", "0", "0" 
     .PlaneNormal "0", "0", "1" 
     .MultipleObjects "True" 
     .GroupObjects "False" 
     .Repetitions "1" 
     .MultipleSelection "False" 
     .Component "" 
     .Material "" 
     .MirrorAdvanced 
End With 


'@ pick edge
Pick.PickEdgeFromId "component1:strip1", "1", "1"


'@ pick edge
Pick.PickEdgeFromId "component1:strip1_1", "1", "1"


'@ define discrete face port: 1
With DiscreteFacePort
     .Reset
     .PortNumber "1"
     .Type "SParameter"
     .Label ""
     .Impedance "73.0"
     .VoltageAmplitude "1.0"
     .SetP1 "True", "25", "0", "-2"
     .SetP2 "True", "25", "0", "2"
     .LocalCoordinates "False"
     .InvertDirection "False"
     .CenterEdge "True"
     .Monitor "True"
     .Create
End With


'@ switch working plane
Plot.DrawWorkplane "false"

BeginHide
	Dim sCommand As String

	'@ define units
	sCommand = ""
	sCommand = sCommand + "With Units " + vbLf
	sCommand = sCommand + ".Geometry ""mm""" + vbLf
	sCommand = sCommand + ".Frequency ""GHz""" + vbLf
	sCommand = sCommand + ".Time ""ns""" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define units", sCommand	
	
	
	'@ define frequency range
	sCommand = ""
	sCommand = sCommand + "With Solver" + vbLf
	sCommand = sCommand + ".FrequencyRange ""0.0"", ""1.5""" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define frequency range", sCommand	


	'@ define background
	sCommand = ""
	sCommand = sCommand + "With Background " + vbLf
	sCommand = sCommand + ".Reset " + vbLf
	sCommand = sCommand + ".Type ""Normal""" + vbLf
	sCommand = sCommand + ".Epsilon ""1.0""" + vbLf
	sCommand = sCommand + ".Mu ""1.0""" + vbLf
	sCommand = sCommand + ".ThermalType ""Normal""" + vbLf
	sCommand = sCommand + ".ThermalConductivity ""0.0""" + vbLf
	sCommand = sCommand + ".XminSpace ""0.0""" + vbLf
	sCommand = sCommand + ".XmaxSpace ""0.0""" + vbLf
	sCommand = sCommand + ".YminSpace ""0.0""" + vbLf
	sCommand = sCommand + ".YmaxSpace ""0.0""" + vbLf
	sCommand = sCommand + ".ZminSpace ""0.0""" + vbLf
	sCommand = sCommand + ".ZmaxSpace ""0.0""" + vbLf
	sCommand = sCommand + ".ApplyInAllDirections ""False""" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define background", sCommand	


	'@ define boundaries
	sCommand = ""
	sCommand = sCommand + "With Boundary" + vbLf
	sCommand = sCommand + ".Xmin ""expanded open""" + vbLf
	sCommand = sCommand + ".Xmax ""expanded open""" + vbLf
	sCommand = sCommand + ".Ymin ""expanded open""" + vbLf
	sCommand = sCommand + ".Ymax ""expanded open""" + vbLf
	sCommand = sCommand + ".Zmin ""expanded open""" + vbLf
	sCommand = sCommand + ".Zmax ""expanded open""" + vbLf
	sCommand = sCommand + ".Xsymmetry ""none""" + vbLf
	sCommand = sCommand + ".Ysymmetry ""magnetic""" + vbLf
	sCommand = sCommand + ".Zsymmetry ""electric""" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define boundaries", sCommand

	
	'@ define e-field monitor
	sCommand = ""
	sCommand = sCommand + "With Monitor" + vbLf
	sCommand = sCommand + "     .Reset" + vbLf
	sCommand = sCommand + "     .Name ""e-field (f=.81)""" + vbLf
	sCommand = sCommand + "     .Dimension ""Volume""" + vbLf
	sCommand = sCommand + "     .Domain ""Frequency""" + vbLf
	sCommand = sCommand + "     .FieldType ""Efield""" + vbLf
	sCommand = sCommand + "     .Frequency "".81""" + vbLf
	sCommand = sCommand + "     .Create" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define monitor: e-field (f=.81)", sCommand

	
	'@ define h-field monitor	
	sCommand = ""
	sCommand = sCommand + "With Monitor" + vbLf
	sCommand = sCommand + "     .Reset" + vbLf
	sCommand = sCommand + "     .Name ""h-field (f=.81)""" + vbLf
	sCommand = sCommand + "     .Dimension ""Volume""" + vbLf
	sCommand = sCommand + "     .Domain ""Frequency""" + vbLf
	sCommand = sCommand + "     .FieldType ""Hfield""" + vbLf
	sCommand = sCommand + "     .Frequency "".81""" + vbLf
	sCommand = sCommand + "     .Create" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define monitor: h-field (f=.81)", sCommand

	
	'@ define farfield monitor
	sCommand = ""
	sCommand = sCommand + "With Monitor" + vbLf
	sCommand = sCommand + "     .Reset" + vbLf
	sCommand = sCommand + "     .Name ""farfield (f=.81)""" + vbLf
	sCommand = sCommand + "     .Domain ""Frequency""" + vbLf
	sCommand = sCommand + "     .FieldType ""Farfield""" + vbLf
	sCommand = sCommand + "     .Frequency "".81""" + vbLf
	sCommand = sCommand + "     .Create" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define farfield monitor: farfield (f=.81)", sCommand

	'@ define farfield monitor
	sCommand = ""
	sCommand = sCommand + "With Monitor" + vbLf
	sCommand = sCommand + "     .Reset" + vbLf
	sCommand = sCommand + "     .Name ""farfield (f=.81)""" + vbLf
	sCommand = sCommand + "     .Domain ""Frequency""" + vbLf
	sCommand = sCommand + "     .FieldType ""Farfield""" + vbLf
	sCommand = sCommand + "     .Frequency "".81""" + vbLf
	sCommand = sCommand + "     .Create" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define farfield monitor: farfield (f=.81)", sCommand

	'@ define farfield monitor
	sCommand = ""
	sCommand = sCommand + "With Monitor" + vbLf
	sCommand = sCommand + "     .Reset" + vbLf
	sCommand = sCommand + "     .Name ""farfield (f=.75)""" + vbLf
	sCommand = sCommand + "     .Domain ""Frequency""" + vbLf
	sCommand = sCommand + "     .FieldType ""Farfield""" + vbLf
	sCommand = sCommand + "     .Frequency "".75""" + vbLf
	sCommand = sCommand + "     .Create" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define farfield monitor: farfield (f=.6)", sCommand

	'@ define farfield monitor
	sCommand = ""
	sCommand = sCommand + "With Monitor" + vbLf
	sCommand = sCommand + "     .Reset" + vbLf
	sCommand = sCommand + "     .Name ""farfield (f=.78)""" + vbLf
	sCommand = sCommand + "     .Domain ""Frequency""" + vbLf
	sCommand = sCommand + "     .FieldType ""Farfield""" + vbLf
	sCommand = sCommand + "     .Frequency "".78""" + vbLf
	sCommand = sCommand + "     .Create" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define farfield monitor: farfield (f=.78)", sCommand

	'@ define farfield monitor
	sCommand = ""
	sCommand = sCommand + "With Monitor" + vbLf
	sCommand = sCommand + "     .Reset" + vbLf
	sCommand = sCommand + "     .Name ""farfield (f=.84)""" + vbLf
	sCommand = sCommand + "     .Domain ""Frequency""" + vbLf
	sCommand = sCommand + "     .FieldType ""Farfield""" + vbLf
	sCommand = sCommand + "     .Frequency "".84""" + vbLf
	sCommand = sCommand + "     .Create" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define farfield monitor: farfield (f=.84)", sCommand

	'@ define farfield monitor
	sCommand = ""
	sCommand = sCommand + "With Monitor" + vbLf
	sCommand = sCommand + "     .Reset" + vbLf
	sCommand = sCommand + "     .Name ""farfield (f=.87)""" + vbLf
	sCommand = sCommand + "     .Domain ""Frequency""" + vbLf
	sCommand = sCommand + "     .FieldType ""Farfield""" + vbLf
	sCommand = sCommand + "     .Frequency "".87""" + vbLf
	sCommand = sCommand + "     .Create" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define farfield monitor: farfield (f=.87)", sCommand

	'@ define solver parameters
	sCommand = ""
	sCommand = sCommand + "With Solver " + vbLf
	sCommand = sCommand + ".CalculationType ""TD-S""" + vbLf
	sCommand = sCommand + ".StimulationPort ""All""" + vbLf
	sCommand = sCommand + ".StimulationMode ""All""" + vbLf
	sCommand = sCommand + ".SteadyStateLimit ""-40""" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "define solver parameters", sCommand	

	
	'@ s-parameter post processing: vswr
	sCommand = ""
	sCommand = sCommand + "With PostProcess1D " + vbLf
	sCommand = sCommand + ".ActivateOperation ""vswr"", ""True""" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "(*) s-parameter post processing: vswr", sCommand

	
	'@ s-parameter post processing: yz-matrices
	sCommand = ""
	sCommand = sCommand + "With PostProcess1D " + vbLf
	sCommand = sCommand + ".ActivateOperation ""yz-matrices"", ""True""" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "(*) s-parameter post processing: yz-matrices", sCommand

	'@ Farfield cuts
	sCommand = ""
	sCommand = sCommand + "With FarfieldPlot" + vbLf
	sCommand = sCommand + " .ClearCuts" + vbLf
	sCommand = sCommand + " .AddCut ""lateral"", ""0"", ""1""" + vbLf
	sCommand = sCommand + " .AddCut ""lateral"", ""45"", ""1""" + vbLf
	sCommand = sCommand + " .AddCut ""lateral"", ""90"", ""1""" + vbLf
	sCommand = sCommand + " .AddCut ""polar"", ""45"", ""1""" + vbLf
	sCommand = sCommand + " .AddCut ""polar"", ""90"", ""1""" + vbLf
	sCommand = sCommand + "End With"
	AddToHistory "(*) define farfield cuts", sCommand

'With FarfieldPlot
'	.ClearCuts ' lateral=phi, polar=theta
'	.AddCut "lateral", "0", "1"
'	.AddCut "lateral", "45", "1"
'	.AddCut "lateral", "90", "1"
'	.AddCut "polar", "45", "1"
'	.AddCut "polar", "90", "1"
'End With

	ResetViewToStructure()
EndHide


mws.SaveAs("C:\\Users\\LCLin\\Desktop\\test.cst", False)
mws.Quit()

' Set studio = Nothing



End Sub



' End Sub