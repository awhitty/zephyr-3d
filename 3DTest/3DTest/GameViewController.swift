//
//  GameViewController.swift
//  3DTest
//
//  Created by Jason van der Merwe on 4/8/15.
//  Copyright (c) 2015 Jason van der Merwe. All rights reserved.
//

import UIKit
import QuartzCore
import SceneKit

class GameViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        
        // create a new scene
        let scene = SCNScene(named: "art.scnassets/trackwithfill")!
        
        // create and add a camera to the scene
        let cameraNode = SCNNode()
        cameraNode.camera = SCNCamera()
        scene.rootNode.addChildNode(cameraNode)
        
        // place the camera
<<<<<<< HEAD
        cameraNode.position = SCNVector3(x: 0, y: 1, z: 20)
=======
        cameraNode.position = SCNVector3(x: 10, y: 1, z: 20)
>>>>>>> 8a873ba7c04c178e4dc8c8214257f82e7e29d328
        cameraNode.rotation = SCNVector4Make(0, 0, 0, 1.5)
        
        // create and add a light to the scene
        let lightNode = SCNNode()
        lightNode.light = SCNLight()
        lightNode.light!.type = SCNLightTypeOmni
<<<<<<< HEAD
        lightNode.position = SCNVector3(x: 0, y: 10, z: 10)
        lightNode.light!.color = UIColor(white: 0.95, alpha: 1.0)
//        lightNode.position = SCNVector3Make(0, 1, 50)
=======
//        lightNode.position = SCNVector3(x: 0, y: 10, z: 10)
        lightNode.light!.color = UIColor(white: 0.75, alpha: 1.0)
        lightNode.position = SCNVector3Make(0, 10, 50)
>>>>>>> 8a873ba7c04c178e4dc8c8214257f82e7e29d328
        scene.rootNode.addChildNode(lightNode)
        
        // create and add an ambient light to the scene
        let ambientLightNode = SCNNode()
        ambientLightNode.light = SCNLight()
        ambientLightNode.light!.type = SCNLightTypeAmbient
<<<<<<< HEAD
        ambientLightNode.light!.color = UIColor.yellowColor()
//        scene.rootNode.addChildNode(ambientLightNode)
        
        let floor = SCNFloor()
        let floorNode = SCNNode(geometry: floor)
        floorNode.position.y = -2.5
        floor.reflectivity = 0
        
        let floorMaterial = SCNMaterial()
        floorMaterial.diffuse.contents  = UIColor.greenColor()
        floorMaterial.locksAmbientWithDiffuse   = true
        floor.materials = [floorMaterial]
        
        scene.rootNode.addChildNode(floorNode)
=======
        ambientLightNode.light!.color = UIColor.darkGrayColor()
        scene.rootNode.addChildNode(ambientLightNode)
>>>>>>> 8a873ba7c04c178e4dc8c8214257f82e7e29d328
        
        // retrieve the ship node
        let ship = scene.rootNode.childNodeWithName("node", recursively: true)!
        ship.scale = SCNVector3(x: 0.02, y: 0.02, z: 0.02)
<<<<<<< HEAD
        ship.position = SCNVector3(x: -10, y: 0, z: 0)
        ship.rotation = SCNVector4Make(1, 0, 0, CFloat( -M_PI_4 ) * 2)
=======
>>>>>>> 8a873ba7c04c178e4dc8c8214257f82e7e29d328
        
        // animate the 3d object
//        ship.runAction(SCNAction.repeatActionForever(SCNAction.rotateByX(0, y: 2, z: 0, duration: 1)))
        
        // retrieve the SCNView
        let scnView = self.view as SCNView
        
        // set the scene to the view
        scnView.scene = scene
        
        // allows the user to manipulate the camera
        scnView.allowsCameraControl = true
        
        // show statistics such as fps and timing information
        scnView.showsStatistics = true
        
        // configure the view
        scnView.backgroundColor = UIColor.blackColor()
        
        // add a tap gesture recognizer
        let tapGesture = UITapGestureRecognizer(target: self, action: "handleTap:")
        var gestureRecognizers = [AnyObject]()
        gestureRecognizers.append(tapGesture)
        if let existingGestureRecognizers = scnView.gestureRecognizers {
            gestureRecognizers.extend(existingGestureRecognizers)
        }
        scnView.gestureRecognizers = gestureRecognizers
    }
    
    func handleTap(gestureRecognize: UIGestureRecognizer) {
        // retrieve the SCNView
        let scnView = self.view as SCNView
        
        // check what nodes are tapped
        let p = gestureRecognize.locationInView(scnView)
        if let hitResults = scnView.hitTest(p, options: nil) {
            // check that we clicked on at least one object
            if hitResults.count > 0 {
                // retrieved the first clicked object
                let result: AnyObject! = hitResults[0]
                
                // get its material
                let material = result.node!.geometry!.firstMaterial!
                
                // highlight it
                SCNTransaction.begin()
                SCNTransaction.setAnimationDuration(0.5)
                
                // on completion - unhighlight
                SCNTransaction.setCompletionBlock {
                    SCNTransaction.begin()
                    SCNTransaction.setAnimationDuration(0.5)
                    
                    material.emission.contents = UIColor.blackColor()
                    
                    SCNTransaction.commit()
                }
                
                material.emission.contents = UIColor.redColor()
                
                SCNTransaction.commit()
            }
        }
    }
    
    override func shouldAutorotate() -> Bool {
        return false
    }
    
    override func prefersStatusBarHidden() -> Bool {
        return true
    }
    
    override func supportedInterfaceOrientations() -> Int {
        if UIDevice.currentDevice().userInterfaceIdiom == .Phone {
            return Int(UIInterfaceOrientationMask.AllButUpsideDown.rawValue)
        } else {
            return Int(UIInterfaceOrientationMask.All.rawValue)
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Release any cached data, images, etc that aren't in use.
    }

}
