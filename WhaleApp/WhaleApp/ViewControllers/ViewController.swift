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
    
    private var type: UploadImage = .first
    
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
        setupDeleteButtonView()
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
        startButton.titleLabel?.font =  .systemFont(ofSize: 18.0, weight: .medium)
        
        startButton.layer.cornerRadius = 16.0
        startButton.layer.masksToBounds = true
        
        startButton.backgroundColor = SColor.accentF.withAlphaComponent(0.5)
    }
    
    private func setupDeleteButtonView() {
        deleteButton.addTarget(self, action: #selector(deleteImages), for: .touchUpInside)
    }
    
    // MARK: -
    
    @objc func deleteImages() {
        firstImageView.image = SImage.plus
        secondImageView.image = SImage.plus
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
        case .second:
            secondImageView.image = image
        }
    }
}
