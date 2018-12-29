#After you import a model, run me to classify and organize the new materials and textures
import unreal
eal = unreal.EditorAssetLibrary

"""
extract and return the path from a loaded asset
@param asset: the asset whose path we wish to aquire 
@returns: the path at which asset is located
"""
def extractAssetPath(asset):
	return str(asset).split("'")[1]

def main():
	modelDir = "/Game/Models"
	textureDir = "/Game/Models/Textures"
	assetNames = unreal.EditorAssetLibrary.list_assets(modelDir,recursive=False)
	existingTextures = unreal.EditorAssetLibrary.list_assets(textureDir,recursive=False)
	for assetName in assetNames:
		asset = eal.load_asset(assetName)
		
		#if a mesh is detected, loop through its materials - prefixing them with the mesh name and moving them into the materials directory
		if (type(asset) == unreal.StaticMesh):
			print("static mesh detected: " + assetName + " -- collecting materials")
			mats = []
			for i in range(99999):
				newMat = asset.get_material(i)
				#stop when we hit the first nonexistent material
				if (newMat == None):
					break
				mats.append(unreal.MaterialInterface.get_base_material(newMat))
			for mat in mats:
				matPath = extractAssetPath(mat)
				#ignore materials that are already in the materials folder
				if ("/Materials/" in matPath):
					continue
				
				#prefix this material name with the corresponding mesh's name and move it into the materials directory
				print("found new material: " + matPath)
				newPath = matPath.replace(modelDir, modelDir + '/Materials/' + assetName.split('.')[-1] + '_')
				newPath = newPath[:newPath.rfind('/')] + newPath[newPath.rfind('/')+1:]
				newPath = newPath[:newPath.rfind('.')]
				eal.rename_loaded_asset(mat,newPath)
		
		#if a texture is detected, check if an identically named texture already exists; if so, consolidate. Otherwise, move this texture into the textures directory
		elif (type(asset) == unreal.Texture2D):
			texPath = extractAssetPath(asset)
			sTexPath = texPath.replace(modelDir,"")
			
			found = None
			for i in existingTextures:
				if (i.replace(textureDir,"") == sTexPath):
					found = eal.load_asset(i)
					break
			#if we found a matching texture name, consolidate
			if (found != None):
				print("texture '" + sTexPath[1:].split('.')[0] + "' already exists; replacing reference and deleting")
				eal.consolidate_assets(found,[asset])
				continue
					
			#no match found; move this texture into the textures directory
			newPath = texPath.replace(modelDir,modelDir + '/Textures')
			newPath = newPath[:newPath.rfind('.')]
			eal.rename_loaded_asset(asset,newPath)

if __name__ == "__main__":
	main()