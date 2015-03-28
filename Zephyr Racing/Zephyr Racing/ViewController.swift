//
//  ViewController.swift
//  Zephyr Racing
//
//  Created by Jason van der Merwe on 3/10/15.
//  Copyright (c) 2015 Jason van der Merwe. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        self.setupView()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
    }
    
    func setupView() {
        var track: TrackLog! = TrackLog(frame: CGRectMake(0, 0, view.frame.width, view.frame.height))
        view.addSubview(track)
        
        
        var track2: TrackLog! = TrackLog(frame: CGRectMake(0, 102, view.frame.width, view.frame.height))
        track2.trackName = "Stent Raceways"
        track2.trackImage = UIImage(named: "track2.png")
        view.addSubview(track2)
    }


}

