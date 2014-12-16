view_controller_template = '''
//
//  {{ upper_name }}{{ upper_view }}ViewController.swift
//
//

import UIKit

class {{ upper_name }}{{ upper_view }}ViewController: UIViewController {
  
  var presenter: {{ upper_name }}Presenter!
  
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
//  {{ upper_name }}Presenter.swift
//
//

import UIKit

class {{ upper_name }}Presenter: NSObject {
  
  var wireframe: {{ upper_name }}Wireframe!
  var interactor: {{ upper_name }}Interactor!

  {% for view in upper_views %}var {{ lower_name }}{{ view }}ViewController: {{ upper_name }}{{ view }}ViewController?
  {% endfor %}
}
'''

interactor = '''
//
//  {{ upper_name }}Interactor.swift
//

import UIKit

class {{ upper_name }}Interactor: NSObject {
  
  var presenter: {{ upper_name }}Presenter!
  
}

'''

wireframe = '''
//
//  {{ upper_name }}Wireframe.swift
//

import UIKit

class {{ upper_name }}Wireframe: NSObject {

  var rootWireFrame: RootWireFrame!
  var presenter: {{ upper_name }}Presenter!

  {% for view in upper_views %}var {{ lower_name }}{{ view }}ViewController: {{ upper_name }}{{ view }}ViewController?
  {% endfor %}
  func {{ lower_name }}Storyboard() -> UIStoryboard {
    let storyboard = UIStoryboard(name: "{{ upper_name }}", bundle: NSBundle.mainBundle())
    return storyboard
  }

}

'''

dependencies_template = '''
//
//  AppDependencies.swift
//

import UIKit

class AppDependencies {
  {% for module in lower_modules %}var {{ module }}Wireframe = {{ upper_modules[loop.index - 1] }}Wireframe()
  {% endfor %}

  //MARK: - Add aditional wireframes here

  init() {
    configureDependencies()
  }
  
  /*
  func installViewControllersIntoWindow(window: UIWindow) {
    // Initialize the root view controller
  }
  */
 
  func configureDependencies() {
    // Root Wireframe
    let rootWire = RootWireFrame()
    {% for module in lower_modules %}

    // MARK: - {{ upper_modules[loop.index - 1] }} Module
    let {{ module }}Presenter = {{ upper_modules[loop.index - 1] }}Presenter()
    let {{ module }}Interactor = {{ upper_modules[loop.index - 1] }}Interactor()

    {{ module }}Interactor.presenter = {{ module }}Presenter
    {{ module }}Presenter.interactor = {{ module }}Interactor
    {{ module }}Presenter.wireframe = {{ module}}Wireframe

    // Instantiate wireframes
    {{ module }}Wireframe.presenter = {{ module }}Presenter
    {{ module }}Wireframe.rootWireFrame = rootWire
    {% endfor %}

    //MARK: - Add Additional Module dependencies here
    ////////////////////////////////////////////////
  }

}

'''

new_dependencies = '''
///////////////////////////// Copy And Paste The Following Output Into AppDependencies.swift ///////////////////

///// Set the following as instance variables /////////
  {% for module in lower_modules %}
  var {{ module }}Wireframe = {{ upper_modules[loop.index - 1] }}Wireframe()
  {% endfor %}

////////////////////////////////////////////////////////





//////// Place the following into configureDependencies() ///////////////////////////////


 {% for module in lower_modules %}
    // MARK: - {{ upper_modules[loop.index - 1] }} Module
    let {{ module }}Presenter = {{ upper_modules[loop.index - 1] }}Presenter()
    let {{ module }}Interactor = {{ upper_modules[loop.index - 1] }}Interactor()

    {{  module }}Interactor.presenter = {{ module }}Presenter
    {{  module }}Presenter.interactor = {{ module }}Interactor
    {{  module }}Presenter.wireframe = {{ module}}Wireframe

    // Instantiate wireframes
    {{  module }}Wireframe.presenter = {{ module }}Presenter
    {{  module }}Wireframe.rootWireFrame = rootWire

 {% endfor %}

    //MARK: - Add Additional Module dependecies here
    ////////////////////////////////////////////////


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

'''

root_wireframe = '''
//
//  RootWireFrame.swift
//

import UIKit

class RootWireFrame: NSObject {
  
   // TODO: Add Initial View Controllers
}

'''

# Watch out for white space if modifying
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