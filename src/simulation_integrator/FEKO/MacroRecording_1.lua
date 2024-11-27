-- CADFEKO v2022-14827 (x64)
app = cf.GetApplication()
project = app.Project

-- New project
project = app:NewProject()

-- Created geometry: cuboid "customCubeOne"
properties = cf.Cuboid.GetDefaultProperties()
properties.Depth = "25.4"
properties.Height = "25.4"
properties.Label = "customCubeOne"
properties.Origin.N = "1"
properties.Origin.U = "1"
properties.Origin.V = "1"
properties.Width = "25.4"
customCubeOne = project.Geometry:AddCuboid(properties)

-- Created geometry: cuboid "Cuboid1"
properties = cf.Cuboid.GetDefaultProperties()
properties.Depth = "25.4"
properties.Height = "25.4"
properties.Label = "Cuboid1"
properties.Origin.N = "1"
properties.Origin.U = "1"
properties.Origin.V = "1"
properties.Width = "25.4"
Cuboid1 = project.Geometry:AddCuboid(properties)
