#When you import a model, run me to rename materials, move them into materials folder, and move textures into textures folder
import unreal
eal = unreal.EditorAssetLibrary

def extractAssetPath(asset):
	matStr = str(asset)
	pathSInd = matStr.find("'")
	pathEInd = matStr.find("'",pathSInd+1)
	texPath = matStr[pathSInd+1:pathEInd]
	return matStr

def main():
	modelDir = "/Game/Models"
	assetNames = unreal.EditorAssetLibrary.list_assets(modelDir)
	for assetName in assetNames:
		asset = eal.load_asset(assetName)
		
		if (type(asset) == unreal.StaticMesh):
			print("static mesh detected: " + assetName + " -- collecting materials")
			mats = []
			for i in range(99999):
				newMat = asset.get_material(i)
				if (newMat == None):
					break
				mats.append(unreal.MaterialInterface.get_base_material(newMat))
			print("found materials:")
			for mat in mats:
				matPath = extractAssetPath(mat)
				#ignore materials that are already in the materials folder
				if ("/Materials/" in matPath):
					continue
				newPath = matPath.replace(modelDir, modelDir + '/Materials/' + assetName.split('.')[-1] + '_')
				newPath = newPath[:newPath.rfind('/')] + newPath[newPath.rfind('/')+1:]
				newPath = newPath[:newPath.rfind('.')]
				eal.rename_loaded_asset(mat,newPath)
		
		elif (type(asset) == unreal.Texture2D):
			texPath = extractAssetPath(asset)
			#ignore textures that are already in the textures folder
			if ("/Textures/" in texPath):
				continue
			newPath = texPath.replace(modelDir,modelDir + '/Textures')
			newPath = newPath[:newPath.rfind('.')]
			eal.rename_loaded_asset(asset,newPath)

if __name__ == "__main__":
	main()