import gvsig
from gvsig import geom
from gvsig.geom import *
from gvsig import uselib

uselib.use_plugin("org.gvsig.topology.app.mainplugin")

import sys

from org.gvsig.topology.lib.spi import AbstractTopologyRule

from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR

import math

from org.gvsig.topology.lib.api import TopologyLocator

from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator

#from DeletePointAction import DeletePointAction


class MustBeLargerThanClusterToleranceLineRule(AbstractTopologyRule):
  
  
  def __init__(self, plan, factory, tolerance, dataSet1):
    #        TopologyPlan plan,
    #        TopologyRuleFactory factory,
    #        double tolerance,
    #        String dataSet1
    
    AbstractTopologyRule.__init__(self, plan, factory, tolerance, dataSet1)
    #self.addAction(DeletePointAction())
  
  def check(self, taskStatus, report, feature1):
    #SimpleTaskStatus taskStatus, 
    #TopologyReport report, 
    #Feature feature1

    try:
      #logger("si", LOGGER_INFO)
      tolerance = self.getTolerance()
      #logger("1", LOGGER_INFO)
      

      line = feature1.getDefaultGeometry()
      #lineTolerance = line.buffer(tolerance)

      if(line==None):
        return

      
      #if(lineTolerance==None):
      #  lineTolerance = line

      #logger("1", LOGGER_INFO)
      theDataSet = self.getDataSet1()
      #logger("2", LOGGER_INFO)
      
      #logger("if", LOGGER_INFO)

      for i in range(0, line.getNumVertices()):
        vertex = line.getVertex(i)
        point = createPoint(D2, vertex.getX(), vertex.getY())
        vertexTolerance = point.buffer(tolerance)
        for j in range(0, line.getNumVertices()):
          otherVertex = line.getVertex(j)
          otherPoint = createPoint(D2, otherVertex.getX(), otherVertex.getY())
          if i == j:
            print "Same vertex"
            continue
          else:
            d = math.sqrt(pow(otherVertex.getX()-vertex.getX(), 2) + pow(otherVertex.getY()-vertex.getY(), 2))
            print d
            print type(vertexTolerance)
            #print tolerance
            if not vertexTolerance.intersects(otherPoint):
              print "The rule is not violated"
            else:
              print "The rule is violated"
              error = line
              report.addLine(self,
                theDataSet,
                None,
                line,
                error,
                None,
                None,
                0,
                0,
                False,
                "The distance between vertices is not larger than the tolerance",
                "Prueba"
              )
              break
            
        #logger("end", LOGGER_INFO)
    except: # Exception as ex:
      #logger("2 Can't check feature."+str(ex), LOGGER_WARN)
      ex = sys.exc_info()[1]
      logger("Can't execute rule. Class Name:" + ex.__class__.__name__ + " Except:" + str(ex))
    finally:
      pass
def main(*args):
  # testing class m = MustBeDisjointPointRule(None, None, 3, None)
  print "* Executing MustBeDisjointPoint RULE main."
  tm = TopologyLocator.getTopologyManager()
  
  from mustBeLargerThanClusterToleranceLineRuleFactory import MustBeLargerThanClusterToleranceLineRuleFactory
  a = MustBeLargerThanClusterToleranceLineRuleFactory()
  tm.addRuleFactories(a)