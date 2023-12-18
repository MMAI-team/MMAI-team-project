import UIKit
import CoreML
import Vision

class AIManager {
    func processImagesWithModel(_ image1: UIImage, _ image2: UIImage) -> Float? {
        guard let model = try? cn(configuration: MLModelConfiguration()) else { return nil }
        
        guard let multiArray1 = preprocess(image1),
              let multiArray2 = preprocess(image2) else { return nil }
        
        let input = cnInput(img_1: multiArray1, img_2: multiArray2)
        
        guard let result = try? model.prediction(input: input) else {
            return nil
        }
        
        return result.Identity[0].floatValue
    }
    
    private func preprocess(_ image: UIImage) -> MLMultiArray? {
        let size = CGSize(width: 224, height: 224)
        
        guard let pixels = image.resize(to: size).pixelData()?.map({ (Double($0) / 255.0 - 0.5) * 2 }) else {
            return nil
        }
        
        guard let array = try? MLMultiArray(shape: [1, 224, 224, 3], dataType: .double) else {
            return nil
        }
        
        let r = pixels.enumerated().filter { $0.offset % 4 == 0 }.map { $0.element }
        let g = pixels.enumerated().filter { $0.offset % 4 == 1 }.map { $0.element }
        let b = pixels.enumerated().filter { $0.offset % 4 == 2 }.map { $0.element }
        
        for i in 0..<224 {
            for j in 0..<224 {
                array[[0, i, j, 0] as [NSNumber]] = NSNumber(value: r[i * 224 + j])
                array[[0, i, j, 1] as [NSNumber]] = NSNumber(value: g[i * 224 + j])
                array[[0, i, j, 2] as [NSNumber]] = NSNumber(value: b[i * 224 + j])
            }
        }
        
        return array
    }
}
