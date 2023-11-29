//
//  ViewController.swift
//  WhaleApp
//
//  Created by Yurii Poberezhnyi on 29.11.2023.
//

import UIKit

class ViewController: UIViewController {
    
    @IBOutlet var contentView: UIView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        setupViews()
    }
    
    // MARK: -
    
    private func setupViews() {
        setupContentView()
    }
    
    private func setupContentView() {
        contentView.backgroundColor = SColor.background
    }
}

