//
//  ViewController.swift
//  WhaleApp
//
//  Created by Yurii Poberezhnyi on 29.11.2023.
//

import UIKit
import Photos

enum UploadImage {
    case first
    case second
}

class ViewController: UIViewController {
    
    @IBOutlet var contentView: GradientView!
    
    @IBOutlet weak var firstView: UIView!
    @IBOutlet weak var secondView: UIView!
    @IBOutlet weak var firstImageView: UIImageView!
    @IBOutlet weak var secondImageView: UIImageView!
    
    @IBOutlet weak var startButton: UIButton!
    
    @IBOutlet weak var deleteButton: UIButton!
    @IBOutlet weak var firstImageDeleteButton: UIButton!
    @IBOutlet weak var secondImageDeleteButton: UIButton!
    
    @IBOutlet weak var resultLabel: UILabel!
    
    private var type: UploadImage = .first
    
    private var firstImage: UIImage?
    private var secondImage: UIImage?
    
    private let model = AIManager()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        setupViews()
    }
    
    // MARK: -
    
    private func setupViews() {
        setupContentView()
        setupFirstView()
        setupSecondView()
        setupStartButtonView()
        setupDeleteButtonsView()
        setupResultLabel()
    }
    
    private func setupContentView() {
        contentView.startColor = SColor.accentF
        contentView.endColor = SColor.accentS
    }
    
    private func setupFirstView() {
        firstView.layer.cornerRadius = 16.0
        firstView.layer.masksToBounds = true
        firstView.backgroundColor = SColor.accentS.withAlphaComponent(0.9)
        
        firstImageView.image = SImage.plus
        firstImageView.layer.cornerRadius = 13.0
        firstImageView.layer.masksToBounds = true
        firstImageView.contentMode = .scaleAspectFill
        
        let tap = UITapGestureRecognizer(target: self, action: #selector(uploadFirstImageTap))
        firstImageView.isUserInteractionEnabled = true
        firstImageView.addGestureRecognizer(tap)
    }
    
    private func setupSecondView() {
        secondView.layer.cornerRadius = 16.0
        secondView.layer.masksToBounds = true
        secondView.backgroundColor = SColor.accentS.withAlphaComponent(0.9)
        
        secondImageView.image = SImage.plus
        secondImageView.layer.cornerRadius = 13.0
        secondImageView.layer.masksToBounds = true
        secondImageView.contentMode = .scaleAspectFill
        
        let tap = UITapGestureRecognizer(target: self, action: #selector(uploadSecondImageTap))
        secondImageView.isUserInteractionEnabled = true
        secondImageView.addGestureRecognizer(tap)
    }
    
    private func setupStartButtonView() {
        startButton.setTitle("Compare", for: .normal)
        startButton.setTitleColor(.white, for: .normal)
        startButton.setTitle("Please upload photos", for: .disabled)
        startButton.setTitleColor(SColor.accentS, for: .disabled)
        startButton.titleLabel?.font =  .systemFont(ofSize: 18.0, weight: .medium)
        
        startButton.layer.cornerRadius = 16.0
        startButton.layer.masksToBounds = true
        
        startButton.backgroundColor = SColor.accentF.withAlphaComponent(0.5)
        
        startButton.addTarget(self, action: #selector(startAction), for: .touchUpInside)
        
        renderStartButton(with: false)
    }
    
    private func setupDeleteButtonsView() {
        deleteButton.addTarget(self, action: #selector(deleteImages), for: .touchUpInside)
        firstImageDeleteButton.addTarget(self, action: #selector(deleteFirstImages), for: .touchUpInside)
        secondImageDeleteButton.addTarget(self, action: #selector(deleteSecondImages), for: .touchUpInside)
    }
    
    private func setupResultLabel() {
        resultLabel.isHidden = true
    }
    
    private func renderStartButton(with state: Bool) {
        startButton.isEnabled = state
        startButton.backgroundColor = (state ? SColor.accentF : .white).withAlphaComponent(0.5)
    }
    
    private func renderResultLabel(with prediction: Int) {
        let text = prediction > 66 ? "It looks similar" : "It looks different"
        print(prediction)
        resultLabel.text = text
        resultLabel.isHidden = false
    }
    
    private func checkIfImagesExist(_ image1: UIImage?, _ image2: UIImage?) -> Bool { image1 != nil && image2 != nil }
    
    // MARK: -
    
    @objc func startAction() {
        if let image1 = firstImage,
           let image2 = secondImage,
           let prediction = model.processImagesWithModel(image1, image2) {
            renderResultLabel(with: Int(prediction))
        }
        else {
            renderStartButton(with: false)
        }
    }
    
    @objc func deleteImages() {
        UIView.transition(with: view, duration: 0.3, options: .transitionCrossDissolve) {
            self.firstImageView.image = SImage.plus
            self.secondImageView.image = SImage.plus
        }
        
        firstImage = nil
        secondImage = nil
        
        resultLabel.isHidden = true
        renderStartButton(with: false)
    }
    
    @objc func deleteFirstImages() {
        UIView.transition(with: view, duration: 0.3, options: .transitionCrossDissolve) { self.firstImageView.image = SImage.plus }
        
        firstImage = nil
        resultLabel.isHidden = true
        renderStartButton(with: false)
    }
    
    @objc func deleteSecondImages() {
        UIView.transition(with: view, duration: 0.3, options: .transitionCrossDissolve) { self.secondImageView.image = SImage.plus }
        
        secondImage = nil
        resultLabel.isHidden = true
        renderStartButton(with: false)
    }
    
    @objc func uploadFirstImageTap() {
        type = .first
        importPicture()
    }
    
    @objc func uploadSecondImageTap() {
        type = .second
        importPicture()
    }
    
    func importPicture() {
        let picker = UIImagePickerController()
        picker.allowsEditing = true
        picker.delegate = self
        present(picker, animated: true)
    }
}

extension ViewController: UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        guard let image = info[.editedImage] as? UIImage else { return }

        dismiss(animated: true)
        
        switch type {
        case .first:
            firstImageView.image = image
            firstImage = image
        case .second:
            secondImageView.image = image
            secondImage = image
        }
        
        let state = checkIfImagesExist(firstImage, secondImage)
        renderStartButton(with: state)
    }
}
