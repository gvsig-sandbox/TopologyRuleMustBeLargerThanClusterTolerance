import gvsig
from gvsig import geom
from gvsig.geom import *
from gvsig import uselib
from org.gvsig.fmap.geom import GeometryUtils

uselib.use_plugin("org.gvsig.topology.app.mainplugin")

import sys

from org.gvsig.topology.lib.spi import AbstractTopologyRule

from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR

import math

from org.gvsig.topology.lib.api import TopologyLocator

from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator

from DeletePointsAction import DeletePointsAction
from DeleteFeatureAction import DeleteFeatureAction


class MustBeLargerThanClusterToleranceRule(AbstractTopologyRule):
  
  
  def __init__(self, plan, factory, tolerance, dataSet1):
    #        TopologyPlan plan,
    #        TopologyRuleFactory factory,
    #        double tolerance,
    #        String dataSet1
    
    AbstractTopologyRule.__init__(self, plan, factory, tolerance, dataSet1)
    self.addAction(DeletePointsAction())
    self.addAction(DeleteFeatureAction())
  
  def check(self, taskStatus, report, feature1):
    #SimpleTaskStatus taskStatus, 
    #TopologyReport report, 
    #Feature feature1

    try:

      geometry = feature1.getDefaultGeometry()
      tolerance = self.getTolerance()
      theDataSet = self.getDataSet1()
      print "id", feature1.Id

      if(geometry==None):
        return

      lista = []
      def errorDetection(geometry):
        for i in range(0, geometry.getNumVertices()):
          vertex = geometry.getVertex(i)
          point = createPoint(D2, vertex.getX(), vertex.getY())
          if tolerance != 0:
            vertexTolerance = point.buffer(tolerance)
          else:
            vertexTolerance = point
          for j in range(0, geometry.getNumVertices()):
            otherVertex = geometry.getVertex(j)
            otherPoint = createPoint(D2, otherVertex.getX(), otherVertex.getY())
            if i == j:
              print "i, j", i, j
              print "Same vertex"
              continue
            else:
              print "i, j", i, j
              if not vertexTolerance.intersects(otherPoint) or vertexTolerance.disjoint(otherPoint):
                print "The rule is not violated"
              else:
                if vertex == otherVertex:
                  print "Geometry's start and end vertices. The rule is not violated"
                else:
                  print "The rule is violated"
                  if otherPoint not in lista:
                    lista.append(otherPoint)
                    print "Point included in the list"
                    print lista
                  else:
                    print "Point not included in the list"

        return lista

      if (GeometryUtils.isSubtype(geom.MULTICURVE, geometry.getGeometryType().getType()) or 
         GeometryUtils.isSubtype(geom.MULTISURFACE, geometry.getGeometryType().getType())):
        for x in range(0, geometry.getPrimitivesNumber()):
          geox = geometry.getPrimitiveAt(x)
          lista = errorDetection(geox)
      else:
        lista = errorDetection(geometry)

      if lista:
        error = createMultiPoint(D2, lista)
        multipoint = error.convertToWKT()
        tolerance = str(tolerance)
        report.addLine(self,
          theDataSet,
          None,
          geometry,
          error,
          feature1.getReference(),
          None,
          0,
          0,
          False,
          "The distance between vertices is not larger than the tolerance",
          tolerance
        )
      else:
        print "No mistakes"

    except:
      ex = sys.exc_info()[1]
      logger("Can't execute rule. Class Name:" + ex.__class__.__name__ + " Except:" + str(ex))
    finally:
      pass
def main(*args):
  print "* Executing MustBeLargerThanClusterTolerance RULE main."
  tm = TopologyLocator.getTopologyManager()
  
  from mustBeLargerThanClusterToleranceLineRuleFactory import MustBeLargerThanClusterToleranceLineRuleFactory
  from mustBeLargerThanClusterTolerancePolygonRuleFactory import MustBeLargerThanClusterTolerancePolygonRuleFactory
  a = MustBeLargerThanClusterToleranceLineRuleFactory()
  b = MustBeLargerThanClusterTolerancePolygonRuleFactory()
  tm.addRuleFactories(a)
  tm.addRuleFactories(b)