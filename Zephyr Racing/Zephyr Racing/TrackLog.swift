//
//  TracksScreen.swift
//  Zephyr Racing
//
//  Created by Megan Faulk on 3/26/15.
//  Copyright (c) 2015 Jason van der Merwe. All rights reserved.
//

import Foundation
import UIKit

@IBDesignable class TrackLog: UIView {
    var view: UIView!
    
    var nibName: String = "TrackLog"
    
    
    @IBOutlet weak var trackImageView: UIImageView!
    @IBOutlet weak var trackNameLabel: UILabel!
    
    
    @IBInspectable var trackImage: UIImage? {
        get {
            return trackImageView.image
        }
        set(image) {
            trackImageView.image = image
        }
    }

    
    @IBInspectable var trackName: String? {
        get {
            return trackNameLabel.text
        }
        set(title) {
            trackNameLabel.text = title
        }
    }
    
    override init(frame: CGRect) {
        // set properties
        super.init(frame: frame)
        self.setup()
    }
    
    required init(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
    }
    
    func setup() {
        view = loadViewFromNib()
        view.frame = bounds
        view.autoresizingMask = UIViewAutoresizing.FlexibleWidth | UIViewAutoresizing.FlexibleHeight
        addSubview(view)
    }
    
    func loadViewFromNib() -> UIView {
        let bundle = NSBundle(forClass: self.dynamicType)
        let nib = UINib(nibName: nibName, bundle: bundle)
        let view = nib.instantiateWithOwner(self, options: nil)[0] as UIView
        return view
    }
}