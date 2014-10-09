viewControllerTemplate = '''
//
//  {{ name.capitalize() }}{{ view.capitalize() }}ViewController.swift
//
//

import UIKit

class {{ name.capitalize() }}{{ view.capitalize() }}ViewController: UIViewController{
  
  var presenter : {{ name }}Presenter?
  
  override func viewDidLoad() {
      super.viewDidLoad()
      // Do any additional setup after loading the view.
  }
  override func viewWillAppear(animated: Bool) {

  }

  override func didReceiveMemoryWarning() {
      super.didReceiveMemoryWarning()
      // Dispose of any resources that can be recreated.
  }

}
'''
presenter = '''
//
//  {{ name }}Presenter.swift
//
//

import UIKit

class {{ name }}Presenter: NSObject {
  
  var wireframe : {{ name }}Wireframe?
  {% for view in viewList%}
  var {{ name.lower() }}{{ view.capitalize() }}ViewController : {{ name.capitalize() }}{{ view.capitalize() }}ViewController?
  {% endfor %}
  var interactor : {{ name }}Interactor?

}
'''
interactor = '''
//
//  {{ name }}Interactor.swift
//

import UIKit

class {{ name.capitalize() }}Interactor: NSObject {
  
  var presenter : {{ name }}Presenter?
  var dataManager : {{ name }}DataManager?
  
}

'''

wireframe = '''
//
//  {{name}}Wireframe.swift
//

import UIKit

class {{ name.capitalize() }}Wireframe: NSObject {
  var rootWireFrame : RootWireFrame?
  var presenter : {{name}}Presenter?

  {% for view in viewList%}
  var {{ name.lower() }}{{ view.capitalize() }}ViewController : {{ name.capitalize() }}{{ view.capitalize() }}ViewController?
  {% endfor %}

  func {{ name.lower() }}Storyboard() -> UIStoryboard{
    let storyboard = UIStoryboard(name: "{{ name.capitalize() }}", bundle: NSBundle.mainBundle())
    return storyboard
  }

}

'''

datamanager = '''
//
//  {{ name }}DataManager.swift
//

import UIKit

class {{ name.capitalize() }}DataManager: NSObject {
  
  var interactor : {{ name }}Interactor?
  
}

'''

dependenciesTemplate = '''
//
//  AppDependencies.swift
//

import UIKit

class AppDependencies {
  
  {% for module in modules %}
	  var {{ module.name.lower() }}Wireframe = {{module.name.capitalize() }}Wireframe()
  {% endfor %}
  
  
  init() {
    configureDependencies()
  }
  
  /*
  func installViewControllersIntoWindow(window: UIWindow){
    // Initialize the root view controller
  }
  */
 
  func configureDependencies(){
    // set up relations to all wireframes
    //Root Wireframe
    let rootWire = RootWireFrame()

    //Data Store
    //TODO: Create DataStore

    {% for module in modules %}
    // MARK: - {{ module.name.capitalize() }} Module
    let {{ module.name.lower() }}Presenter = {{ module.name.capitalize() }}Presenter()
    let {{ module.name.lower() }}Interactor = {{ module.name.capitalize() }}Interactor()
    let {{ module.name.lower() }}DataManager = {{ module.name.capitalize() }}DataManager()

    {{ module.name.lower() }}Interactor.presenter = {{ module.name.lower() }}Presenter
    {{ module.name.lower() }}Interactor.dataManager = {{ module.name.lower() }}DataManager
    {{ module.name.lower() }}Presenter.interactor = {{ module.name.lower() }}Interactor
    {{ module.name.lower() }}Presenter.wireframe = {{ module.name.lower() }}Wireframe
    {{ module.name.lower() }}DataManager.interactor = {{ module.name.lower() }}Interactor
    //TODO: Set the DataMangaers DataStore

    // Instantiate wireframes
    {{ module.name.lower() }}Wireframe.presenter = {{ module.name.lower() }}Presenter
    {{ module.name.lower() }}Wireframe.rootWireFrame = rootWire

    //TODO: Configure {{ module.name.capitalize() }} DataManager 
    {% endfor %}
  }

}

'''
rootWireframe = '''
//
//  RootWireFrame.swift
//

import UIKit

class RootWireFrame: NSObject, UITabBarDelegate {
  
   // TODO: Add Initial View Controllers
}

'''
## Watch out for white space if modifying
storyboard = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<document type="com.apple.InterfaceBuilder3.CocoaTouch.Storyboard.XIB" version="3.0" toolsVersion="6211" systemVersion="14A298i" targetRuntime="iOS.CocoaTouch" propertyAccessControl="none" useAutolayout="YES" useTraitCollections="YES" initialViewController="vXZ-lx-hvc">
    <dependencies>
        <plugIn identifier="com.apple.InterfaceBuilder.IBCocoaTouchPlugin" version="6204"/>
    </dependencies>
    <scenes>
        <!--View Controller-->
        <scene sceneID="ufC-wZ-h7g">
            <objects>
                <viewController id="vXZ-lx-hvc" customClass="ViewController" customModuleProvider="target" sceneMemberID="viewController">
                    <layoutGuides>
                        <viewControllerLayoutGuide type="top" id="jyV-Pf-zRb"/>
                        <viewControllerLayoutGuide type="bottom" id="2fi-mo-0CV"/>
                    </layoutGuides>
                    <view key="view" contentMode="scaleToFill" id="kh9-bI-dsS">
                        <rect key="frame" x="0.0" y="0.0" width="600" height="600"/>
                        <autoresizingMask key="autoresizingMask" flexibleMaxX="YES" flexibleMaxY="YES"/>
                        <color key="backgroundColor" white="1" alpha="1" colorSpace="custom" customColorSpace="calibratedWhite"/>
                    </view>
                </viewController>
                <placeholder placeholderIdentifier="IBFirstResponder" id="x5A-6p-PRh" sceneMemberID="firstResponder"/>
            </objects>
        </scene>
    </scenes>
</document>'''