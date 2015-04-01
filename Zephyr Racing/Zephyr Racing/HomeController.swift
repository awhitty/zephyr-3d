//
//  HomeController.swift
//  Zephyr Racing
//
//  Created by Jason van der Merwe on 3/25/15.
//  Copyright (c) 2015 Jason van der Merwe. All rights reserved.
//

import UIKit

class HomeController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        self.setupViews()
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        
        view.backgroundColor = UIColor.orangeColor();
    }
   
    func setupViews(){
        var view1: UIView! = UIView()
        view1.frame = CGRectMake(0, 0, 100, 100)
        view1.backgroundColor = UIColor.purpleColor()
        view.addSubview(view1)
    }

}
